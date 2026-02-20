import pandas as pd
from pathlib import Path


class DatasetLoaderError(Exception):
    pass


def load_dataset(path: str):

    path_obj = Path(path)

    if not path_obj.exists():
        raise DatasetLoaderError(f"Dataset not found: {path}")

    if path_obj.stat().st_size == 0:
        raise DatasetLoaderError(f"Dataset is empty: {path}")

    ext = path_obj.suffix.lower()

    try:

        if ext == ".csv":
            df = pd.read_csv(path)

        elif ext == ".tsv":
            df = pd.read_csv(path, sep="\t")

        elif ext == ".json":
            df = pd.read_json(path)

        elif ext == ".jsonl":
            df = pd.read_json(path, lines=True)

        elif ext == ".parquet":
            df = pd.read_parquet(path)

        else:
            raise DatasetLoaderError(
                f"Unsupported file format: {ext}"
            )

    except Exception as e:
        raise DatasetLoaderError(f"Failed to load dataset: {e}")

    if df.empty:
        raise DatasetLoaderError("Dataset contains no rows")

    if len(df.columns) == 0:
        raise DatasetLoaderError("Dataset contains no columns")

    return df