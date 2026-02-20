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

## 🧠 Recommended Models for Translation (Ollama)

The following models are fully compatible with Ollama and provide excellent multilingual translation performance.

| Model | Parameters | Quality | Speed | RAM Required | Recommendation | Notes |
|------|------------|---------|-------|--------------|----------------|------|
| **qwen3:14b** ⭐ | 14B | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 16–24 GB | 🥇 Best overall | Best balance of quality and performance |
| **qwen3:32b** | 32B | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | 32–48 GB | 🥇 Best quality | Highest translation accuracy |
| **qwen3:8b** | 8B | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 8–12 GB | 🥇 Best for laptops | Fast and efficient |
| **mixtral:8x7b** | 46B (MoE) | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | 32+ GB | 🥇 Production use | Extremely strong multilingual performance |
| **gemma3:27b** | 27B | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | 24–32 GB | 🥇 Excellent alternative | Very stable translations |
| **command-r-plus** | 104B | ⭐⭐⭐⭐⭐ | ⭐⭐ | 48+ GB | 🥇 Enterprise | Best instruction-following |
| **gemma3:12b** | 12B | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 12–16 GB | 🥈 Recommended | Great balance |
| **mistral-small3.2** | 24B | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 16–24 GB | 🥈 Recommended | Fast and reliable |
| **phi3.5:medium** | 14B | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 12–16 GB | 🥈 Lightweight | Efficient and capable |
| **qwen3:4b** | 4B | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 6–8 GB | 🥉 Lightweight | Good for low-resource systems |

---

## 🥇 Best Model by Hardware

| Hardware | Recommended Model |
|--------|------------------|
| 8 GB RAM | qwen3:4b |
| 16 GB RAM | qwen3:8b ⭐ |
| 24 GB RAM | qwen3:14b ⭐⭐⭐ |
| 32 GB RAM | gemma3:27b or mixtral:8x7b |
| 48+ GB RAM | qwen3:32b or command-r-plus |

---

## 🚀 Installation example

```bash
ollama pull qwen3:14b
```
---

## 📜 License

MIT License

---

## ⭐ If you like this project, consider giving it a star!
