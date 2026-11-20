import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from idi import integrate
from idi.schema_matcher import match_columns

DATA = os.path.join(os.path.dirname(__file__), "..", "data")


def test_schema_matching():
    m = match_columns(["Customer Name", "E-mail", "Mobile", "Town", "Joined"])
    assert m["Customer Name"] == "name" and m["E-mail"] == "email"


def test_integration_dedupes():
    result = integrate(DATA, verbose=False)
    assert len(result) == 5  # John, Priya, Rahul, Anita, Karan
    john = result[result["name"].str.contains("John")].iloc[0]
    assert john["records_merged"] == 3
