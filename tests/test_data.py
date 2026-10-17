import pytest

from bank.data import ROWS, EXPORT
import pandera.pandas as pa

# С данными все норм
def test_validation(bank_test):
    ROWS.validate(bank_test)

def test_reject_invalid_age(bank_test):
    bank_test.loc[0, 'age'] = 10

    with pytest.raises(pa.errors.SchemaErrors):
        ROWS.validate(bank_test, lazy = True)

def test_reject_invalid_day_of_week(bank_test):
    bank_test.loc[0, 'day_of_week'] = 'sun'
    with pytest.raises(pa.errors.SchemaErrors) as e:
        ROWS.validate(bank_test, lazy = True)
    
    assert len(e.value.failure_cases) == 1
    assert set(e.value.failure_cases["column"]) == {'day_of_week'}

def test_export_small_rejected(bank_test):
    with pytest.raises(pa.errors.SchemaErrors) as e:
        EXPORT.validate(bank_test, lazy = True)

    expected_mistake = "Слишком маленький датасет. Меньше 10 тысяч строк"

    assert expected_mistake in e.value.failure_cases["check"].values

