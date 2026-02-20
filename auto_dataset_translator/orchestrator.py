from auto_dataset_translator.dataset.loader import load_dataset
from auto_dataset_translator.dataset.writer import write_dataset
from auto_dataset_translator.translator.ollama_client import OllamaClient

from tqdm import tqdm


def run(
    input_path,
    output_path,
    columns,
    model,
    target_lang,
    source_lang=None,
):

    print("Loading dataset...")
    df = load_dataset(input_path)

    print("Initializing translator...")
    translator = OllamaClient(
        model=model,
        target_lang=target_lang,
        source_lang=source_lang,
    )

    for col in columns:

        if col not in df.columns:
            raise ValueError(f"Column '{col}' not found")

        print(f"Translating column: {col}")

        df[col] = [
            translator.translate(text)
            for text in tqdm(df[col])
        ]

    print("Writing output dataset...")
    write_dataset(df, output_path)

    print("Done.")