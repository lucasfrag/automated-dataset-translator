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

    parser.add_argument(
        "--workers",
        "-w",
        type=int,
        default=1,
        help="Number of parallel workers"
    )

    parser.add_argument(
        "--max-retries",
        type=int,
        default=5,
        help="Maximum retry attempts"
    )

    parser.add_argument(
        "--retry-delay",
        type=float,
        default=1.0,
        help="Base retry delay in seconds"
    )

    return parser.parse_args()