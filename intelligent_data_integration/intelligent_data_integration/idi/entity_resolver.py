"""Entity resolution: find records that refer to the same real-world entity."""
from difflib import SequenceMatcher
from itertools import combinations
import pandas as pd


def _same(a, b) -> bool:
    return pd.notna(a) and pd.notna(b) and a == b


def similarity(r1, r2) -> float:
    """Score in [0, 1]. Exact email/phone match is strong evidence."""
    if _same(r1["email"], r2["email"]):
        return 1.0
    score = 0.0
    if pd.notna(r1["name"]) and pd.notna(r2["name"]):
        score += 0.7 * SequenceMatcher(None, r1["name"].lower(), r2["name"].lower()).ratio()
    if _same(r1["phone"], r2["phone"]):
        score += 0.3
    elif _same(r1["city"], r2["city"]):
        score += 0.1
    return score


def resolve(df: pd.DataFrame, threshold: float = 0.85) -> pd.DataFrame:
    """Add a `cluster_id` column using union-find over similar pairs."""
    df = df.reset_index(drop=True)
    parent = list(range(len(df)))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for i, j in combinations(range(len(df)), 2):
        if similarity(df.loc[i], df.loc[j]) >= threshold:
            parent[find(i)] = find(j)

    df["cluster_id"] = [find(i) for i in range(len(df))]
    return df
