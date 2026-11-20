"""Load heterogeneous data sources (CSV / JSON) into DataFrames."""
import os
import pandas as pd


def load_source(path: str) -> pd.DataFrame:
    ext = os.path.splitext(path)[1].lower()
    if ext == ".csv":
        df = pd.read_csv(path, dtype=str)
    elif ext == ".json":
        df = pd.read_json(path, dtype=str)
    else:
        raise ValueError(f"Unsupported file type: {ext}")
    df["_source"] = os.path.basename(path)
    return df


def load_all(folder: str) -> list:
    files = sorted(
        os.path.join(folder, f)
        for f in os.listdir(folder)
        if f.lower().endswith((".csv", ".json"))
    )
    return [load_source(f) for f in files]
