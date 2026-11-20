"""End-to-end pipeline: load -> align -> clean -> resolve -> merge."""
import pandas as pd
from .loader import load_all
from .schema_matcher import align, CANONICAL_SCHEMA
from .cleaner import clean
from .entity_resolver import resolve


def merge_clusters(df: pd.DataFrame) -> pd.DataFrame:
    """Collapse each cluster into one golden record (first non-null value wins)."""
    rows = []
    for cid, group in df.groupby("cluster_id"):
        rec = {}
        for col in CANONICAL_SCHEMA:
            vals = group[col].dropna()
            rec[col] = vals.iloc[0] if len(vals) else None
        rec["sources"] = ", ".join(sorted(set(group["_source"])))
        rec["records_merged"] = len(group)
        rows.append(rec)
    return pd.DataFrame(rows)


def integrate(folder: str, threshold: float = 0.85, verbose: bool = True) -> pd.DataFrame:
    frames = []
    for raw in load_all(folder):
        aligned, mapping = align(raw)
        if verbose:
            print(f"[schema] {raw['_source'].iloc[0]}: {mapping}")
        frames.append(clean(aligned))
    combined = pd.concat(frames, ignore_index=True)
    if verbose:
        print(f"[load] {len(combined)} total records")
    resolved = resolve(combined, threshold)
    result = merge_clusters(resolved)
    if verbose:
        print(f"[resolve] {len(result)} unique entities")
    return result
