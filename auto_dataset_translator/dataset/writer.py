from pathlib import Path


def write_dataset(df, path: str):

    ext = Path(path).suffix.lower()

    if ext == ".csv":
        df.to_csv(path, index=False)

    elif ext == ".json":
        df.to_json(path, orient="records", indent=2, force_ascii=False)

    elif ext == ".jsonl":
        df.to_json(path, orient="records", lines=True, force_ascii=False)

    elif ext == ".parquet":
        df.to_parquet(path, index=False)

    else:
        raise ValueError(f"Unsupported format: {ext}")