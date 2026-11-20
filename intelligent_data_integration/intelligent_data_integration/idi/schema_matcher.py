"""Schema matching: map each source's columns onto a canonical schema
using synonyms + fuzzy string similarity."""
from difflib import SequenceMatcher
import re

CANONICAL_SCHEMA = {
    "name": ["name", "full name", "customer name", "contact name", "client"],
    "email": ["email", "e-mail", "mail", "email address", "contact email"],
    "phone": ["phone", "mobile", "telephone", "contact number", "phone number"],
    "city": ["city", "town", "location"],
    "signup_date": ["signup date", "joined", "registration date", "created at", "date"],
}


def _norm(text: str) -> str:
    return re.sub(r"[\W_]+", " ", text.lower()).strip()


def match_columns(columns, threshold: float = 0.7) -> dict:
    """Return {source_column: canonical_column} for confident matches."""
    mapping, used = {}, set()
    for col in columns:
        if col.startswith("_"):
            continue
        best, best_score = None, 0.0
        for canon, synonyms in CANONICAL_SCHEMA.items():
            for syn in synonyms:
                score = SequenceMatcher(None, _norm(col), syn).ratio()
                if score > best_score:
                    best, best_score = canon, score
        if best and best_score >= threshold and best not in used:
            mapping[col] = best
            used.add(best)
    return mapping


def align(df):
    """Rename columns to the canonical schema and add missing ones."""
    mapping = match_columns(df.columns)
    out = df.rename(columns=mapping)
    keep = list(CANONICAL_SCHEMA) + ["_source"]
    for c in keep:
        if c not in out.columns:
            out[c] = None
    return out[keep], mapping
