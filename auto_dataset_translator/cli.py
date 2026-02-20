import argparse


def parse_args():

    parser = argparse.ArgumentParser(
        description="Automatic Dataset Translator using Ollama"
    )

    parser.add_argument(
        "--input",
        "-i",
        required=True,
        help="Input dataset path"
    )

    parser.add_argument(
        "--output",
        "-o",
        required=True,
        help="Output dataset path"
    )

    parser.add_argument(
        "--columns",
        "-c",
        required=True,
        nargs="+",
        help="Columns to translate"
    )

    parser.add_argument(
        "--model",
        "-m",
        required=True,
        help="Ollama model name"
    )

    parser.add_argument(
        "--target-lang",
        "-t",
        required=True,
        help="Target language"
    )

    parser.add_argument(
        "--source-lang",
        "-s",
        required=False,
        help="Source language (optional)"
    )

    return parser.parse_args()