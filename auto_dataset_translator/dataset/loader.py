import pandas as pd
from pathlib import Path


def load_dataset(path: str):

    ext = Path(path).suffix.lower()

    if ext == ".csv":
        return pd.read_csv(path)

    elif ext == ".json":
        return pd.read_json(path)

    elif ext == ".jsonl":
        return pd.read_json(path, lines=True)

    elif ext == ".parquet":
        return pd.read_parquet(path)

    else:
        raise ValueError(f"Unsupported format: {ext}")