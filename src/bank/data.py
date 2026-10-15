import pandas as pd
import os
import sys
from pathlib import Path

import pandas as pd
import pandera.pandas as pa

RAW_PATH = Path(os.getenv("DATA_PATH", 'datasets/bank_additional_pre.csv'))
EXPERIMENT = os.getenv("EXPERIMENT", 'bank_experiment')

# Правила для каждой строки
ROWS = pa.DataFrameSchema(
    {
        "age": pa.Column(pa.Int64),
        "job": pa.Column(pa.String),
        "emp.var.rate": pa.Column(pa.String),
        "cons.conf.idx": pa.Column(pa.String),
        "euribor3m": pa.Column(pa.String),
        "nr.employed": pa.Column(pa.String),
        "job": pa.Column(pa.String),
        "education": pa.Column(pa.String),
        "month": pa.Column(pa.String),
        "day_of_week": pa.Column(pa.String),
        "y": pa.Column(pa.String, pa.Check.str_isin(["yes", "no"])),
    }
)