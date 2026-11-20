# Intelligent Data Integration

A simple base project that integrates customer data from multiple heterogeneous
sources (CSV / JSON) into one clean, de-duplicated dataset.

## Pipeline
1. **Load** – read every CSV/JSON file in `data/`.
2. **Schema matching** – map differing column names (e.g. `Mobile`, `telephone`,
   `phone number`) to a canonical schema using synonyms + fuzzy matching.
3. **Cleaning** – normalise names, emails, phones, cities and dates.
4. **Entity resolution** – detect duplicate people across sources (email match,
   fuzzy name + phone/city similarity) with union-find clustering.
5. **Merge** – build one "golden record" per entity, tracking contributing sources.

## Run
```bash
pip install -r requirements.txt
python main.py                      # uses ./data, writes integrated_output.csv
python main.py --input my_folder --threshold 0.8
pytest                              # run tests
```

## Project layout
```
main.py                 CLI entry point
idi/loader.py           file loading
idi/schema_matcher.py   column mapping
idi/cleaner.py          value normalisation
idi/entity_resolver.py  duplicate detection
idi/integrator.py       pipeline + merging
data/                   sample sources
tests/                  unit tests
```

## Ideas to extend
- Add database / API sources, ML-based matching, blocking for large data,
  a Streamlit/Flask UI, or per-field conflict-resolution rules.
