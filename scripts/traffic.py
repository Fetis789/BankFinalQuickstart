import argparse
import json
import random
import time
import urllib.error
import urllib.request

import pandas as pd

pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)
pd.set_option("display.max_colwidth", 50)

parser = argparse.ArgumentParser()
parser.add_argument("--url", default="http://bank.localhost")
parser.add_argument("--rps", type=float, default=5)
parser.add_argument("--bad", type=float, default=0.0)
parser.add_argument("--recs", type=int, default=0)
args = parser.parse_args()

df = pd.read_csv("datasets/bank_additional_pre.csv", sep = ';')

TARGET = 'y'
NUMERIC = ['age', 'campaign', 'emp.var.rate', 'cons.conf.idx', 'euribor3m', 'nr.employed']
CATEGORICAL = ['job', 'education', 'month', 'day_of_week']
NUMERIC_MEDIANS = {'age': 38.0, 'campaign': 2.0, 'emp.var.rate': 1.1, 
    'cons.conf.idx': -41.8, 'euribor3m': 4.857, 'nr.employed': 5191.0}

NEED_FEATS = NUMERIC + CATEGORICAL
print(NEED_FEATS)
print(df.columns)

df = df[NEED_FEATS]
for column in CATEGORICAL:
    df[column] = df[column].fillna("__MISSING__").astype(str)

for column in NUMERIC:
    df[column] = pd.to_numeric(df[column], errors="coerce")
    df[column] = df[column].fillna(NUMERIC_MEDIANS[column])

rows = [{k: (None if v is None else v) for k, v in r.items()} 
        for r in df.to_dict("records")]

codes = {}
start = time.time()
for _ in range(args.recs):
    row = dict(random.choice(rows))
    if random.random() < args.bad:
        row['campaign'] = 'two'
    
    req = urllib.request.Request(f"{args.url}/v1/predict", json.dumps(row).encode(), 
            method="POST", headers={"Content-Type": "application/json"})
    
    try:
        with urllib.request.urlopen(req, timeout = 5) as resp:
            code = resp.status
    except urllib.error.HTTPError as e:
        code = e.code
    except (urllib.error.URLError, OSError):
        code = 0
    
    codes[code] = codes.get(code, 0) + 1
    total = sum(codes.values())
    if total % 50 == 0:
        print(f"{total} запросов за {time.time() - start:.2f} секунд, коды {codes}", flush = True)
    
    time.sleep(1/args.rps)
