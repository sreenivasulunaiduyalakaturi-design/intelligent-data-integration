"""Normalise values so records from different sources are comparable."""
import re
import pandas as pd


def clean(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["name"] = df["name"].astype("string").str.strip().str.replace(r"\s+", " ", regex=True).str.title()
    df["email"] = df["email"].astype("string").str.strip().str.lower()
    df["phone"] = df["phone"].apply(_clean_phone)
    df["city"] = df["city"].astype("string").str.strip().str.title()
    df["signup_date"] = df["signup_date"].apply(_clean_date)
    return df


def _clean_phone(value):
    if value is None or pd.isna(value):
        return None
    digits = re.sub(r"\D", "", str(value))
    return digits[-10:] if len(digits) >= 10 else (digits or None)


def _clean_date(value):
    if value is None or pd.isna(value):
        return None
    text = str(value).strip()
    # ISO dates (YYYY-MM-DD) must not be parsed day-first; other formats are.
    iso = bool(re.match(r"^\d{4}-\d{2}-\d{2}", text))
    parsed = pd.to_datetime(text, errors="coerce", dayfirst=not iso)
    return None if pd.isna(parsed) else parsed.strftime("%Y-%m-%d")
