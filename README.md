# 🌍 Automated Dataset Translator

> Automatically translate structured datasets (CSV, JSON, JSONL, TSV, Parquet) using LLMs via Ollama — with caching, parallelism, checkpointing, and retry support.

---

## ✨ Features

* 🌐 Translate dataset **content automatically using LLMs**
* 📂 Supports multiple formats:

  * CSV
  * JSON
  * JSONL
  * TSV
  * Parquet
* 🧠 Uses **local models via Ollama**
* ⚡ Parallel processing (multi-threaded)
* 💾 Persistent cache (SQLite) — avoids retranslating identical text
* 🔁 Automatic retry with exponential backoff
* ⏸️ Checkpoint system — resume interrupted translations
* 📊 Progress bars with tqdm
* 🎯 Select specific columns to translate
* 🔒 Safe and deterministic output generation

---

## 📦 Installation

Clone the repository:

```bash
git clone https://github.com/lucasfrag/auto-dataset-translator.git
cd auto-dataset-translator
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Install Ollama:

https://ollama.ai

Pull a model:

```bash
ollama pull llama3.1:8b
```

---

## 🚀 Usage

Basic example:

```bash
python main.py \
  --input dataset.csv \
  --output dataset_pt.csv \
  --columns text title description \
  --model llama3.1:8b \
  --target-lang Portuguese
```

---

## ⚡ Parallel processing

Use multiple workers:

```bash
python main.py \
  -i dataset.csv \
  -o dataset_pt.csv \
  -c text title description \
  -m llama3.1:8b \
  -t Portuguese \
  -w 4
```

---

## 🔁 Force retranslation

Ignore cache and checkpoint:

```bash
python main.py ... --force
```

---

## 🧠 How it works

Pipeline:

```
Load dataset
   ↓
Check cache
   ↓
Translate using Ollama
   ↓
Save to cache
   ↓
Save checkpoint
   ↓
Write output dataset
```

---

## 💾 Cache system

Cache is stored in:

```
translation_cache.db
```

Benefits:

* Avoid retranslating identical text
* Massive performance improvements
* Persistent across runs

---

## ⏸️ Checkpoint system

Checkpoint is stored in:

```
checkpoint.db
```

Allows:

* Resume interrupted runs
* Process very large datasets safely
* Crash recovery

---

## 🎯 Example

Input:

```csv
text,title
Hello world,Greeting
Machine learning is amazing,Statement
```

Output:

```csv
text,title
Olá mundo,Saudação
Aprendizado de máquina é incrível,Declaração
```

---

## ⚙️ Arguments

| Argument              | Description                 |
| --------------------- | --------------------------- |
| `--input`, `-i`       | Input dataset               |
| `--output`, `-o`      | Output dataset              |
| `--columns`, `-c`     | Columns to translate        |
| `--model`, `-m`       | Ollama model                |
| `--target-lang`, `-t` | Target language             |
| `--source-lang`, `-s` | Source language (optional)  |
| `--workers`, `-w`     | Parallel workers            |
| `--force`             | Ignore cache and checkpoint |
| `--reset-cache`       | Delete cache                |
| `--reset-checkpoint`  | Delete checkpoint           |
| `--max-retries`       | Retry attempts              |
| `--retry-delay`       | Base retry delay            |

---

## ⚡ Performance

Features designed for scalability:

* Parallel processing
* Persistent caching
* Checkpoint resume
* Thread-safe SQLite backend

---

## 🛠️ Requirements

* Python 3.9+
* Ollama

---

## 📜 License

MIT License

---

## ⭐ If you like this project, consider giving it a star!
