from auto_dataset_translator.dataset.loader import load_dataset
from auto_dataset_translator.dataset.writer import write_dataset
from auto_dataset_translator.translator.ollama_client import OllamaClient

from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm


def translate_column(df, column, translator, workers):

    texts = df[column].tolist()

    if workers == 1:

        return [
            translator.translate(text)
            for text in tqdm(texts)
        ]

    else:

        with ThreadPoolExecutor(max_workers=workers) as executor:

            results = list(
                tqdm(
                    executor.map(translator.translate, texts),
                    total=len(texts)
                )
            )

        return results


def run(
    input_path,
    output_path,
    columns,
    model,
    target_lang,
    source_lang=None,
    workers=1,
):

    print("Loading dataset...")
    df = load_dataset(input_path)

    print("Initializing translator...")
    translator = OllamaClient(
        model=model,
        target_lang=target_lang,
        source_lang=source_lang,
    )

    print(f"Using {workers} workers")

    for col in columns:

        if col not in df.columns:
            raise ValueError(f"Column '{col}' not found")

        print(f"Translating column: {col}")

        df[col] = translate_column(
            df,
            col,
            translator,
            workers
        )

    print("Writing output dataset...")
    write_dataset(df, output_path)

    print("Done.")