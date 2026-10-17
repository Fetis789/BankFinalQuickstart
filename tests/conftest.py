import pytest
from fastapi.testclient import TestClient
import pandas as pd

from bank.service.app import app


@pytest.fixture(scope ="session")
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture()
def good_row():
    return {
        "euribor3m": 4.857,
        "nr.employed": 5191.0,
        "month": "may",
        "campaign": 2,
        "job": "technician",
        "education": "professional.course",
        "age": 42,
        "emp.var.rate": -1.8,
        "cons.conf.idx": -46.2,
        "day_of_week": "mon"
        }

@pytest.fixture()
def bad_row():
    return {
        "euribor3m": 4.857,
        "nr.employed": 5191.0,
        "month": "may",
        "campaign": 'two',
        "job": "technician",
        "education": "professional.course",
        "age": 42,
        "emp.var.rate": -1.8,
        "cons.conf.idx": -46.2,
        "day_of_week": "mon"
        }

@pytest.fixture()
def bank_test():
    return pd.DataFrame({
        "age": [18, 45, 58],
        "campaign": [10, 20, 30],
        "emp.var.rate": [-1.8, -2.1, -2.4],
        "cons.conf.idx": [-46.2, -47.1, -48.0],
        "euribor3m": [4.857, 5.123, 5.389],
        "nr.employed": [5191.0, 5255.0, 5319.0],
        "month": ["jan", "feb", "mar"],
        "job": ["technician", "services", "management"],
        "education": ["professional.course", "university.degree", "basic.4y"],
        "day_of_week": ["mon", "tue", "wed"],
        "y": ["yes", "no", "yes"]
    })

