# Custom CSV Parser in Python

This project implements a custom CSV (Comma-Separated Values) reader and writer from scratch in Python. It is designed to mimic the core behavior of Python’s built‑in `csv` module while exposing the low‑level mechanics of text parsing, quoting, and file I/O that are important for data engineering work. [web:22][web:43]

---

## 1. Project Overview

The project contains two main classes:

- `CustomCsvReader`: Streams CSV data row by row from a file using a simple state machine that processes the file character by character. It correctly handles commas, quoted fields, escaped double quotes, and embedded newlines inside quoted fields. [web:22][web:43]
- `CustomCsvWriter`: Serializes lists of values to CSV format, automatically quoting fields that contain commas, double quotes, or newline characters, and escaping internal double quotes by doubling them. [web:42][web:60]

Together these components demonstrate how to parse and serialize CSV files without relying on external packages, while also enabling performance comparison against the standard library.

---

## 2. Project Structure

The repository is organized as follows:

- `custom_csv.py`  
  Contains the `CustomCsvReader` and `CustomCsvWriter` classes, along with a small manual round‑trip test when run as a script. [web:22]
- `generate_data.py`  
  Generates a synthetic CSV file (`benchmark_data.csv`) with at least 10,000 rows and 5 columns, including edge cases such as commas, quotes, and newlines in fields. [web:84]
- `benchmark.py`  
  Benchmarks read and write performance of the custom reader/writer against Python’s built‑in `csv.reader` and `csv.writer` using a high‑resolution timer. [web:77][web:81][web:92]
- `requirements.txt`  
  Lists Python dependencies. The implementation only uses the standard library, so this file mainly documents that no third‑party packages are required. [web:22]
- `README.md`  
  This documentation file.

---

## 3. Setup Instructions

1. **Clone the repository**

git clone https://github.com/GowthamiAkula/custom_csv_parser
cd custom_csv_parser


2. **Create and activate a virtual environment (optional but recommended)**

python -m venv .venv
source .venv/Scripts/activate # Windows PowerShell / Git Bash


3. **Install dependencies**

pip install -r requirements.txt


The code uses only Python’s standard library modules such as `csv`, `time`, and `random`, so this step is mainly for completeness. [web:22]

4. **Verify the basic test**
python custom_csv.py


This script runs a small round‑trip test that writes a sample CSV file with edge cases and then reads it back using the custom reader and writer. The printed rows should match the original data, including values with commas, quotes, and embedded newlines. [web:22][web:42]

---

## 4. Usage Examples

### 4.1 Reading CSV with `CustomCsvReader`

The custom reader is implemented as an iterator that yields one row (list of strings) at a time without loading the whole file into memory, which is important for large datasets. [web:22][web:43]

from custom_csv import CustomCsvReader

with open("input.csv", "r", newline="") as f:
reader = CustomCsvReader(f)
for row in reader:
# row is a list of strings representing one CSV record
print(row)


Features:

- Treats commas as separators only when outside quotes. [web:43]
- Interprets `""` inside a quoted field as a single `"` character. [web:64][web:65]
- Preserves newline characters that appear inside quoted fields instead of splitting the record there. [web:55]

### 4.2 Writing CSV with `CustomCsvWriter`

The writer accepts rows as lists or tuples, escapes quotes by doubling them, and quotes fields only when necessary. [web:42][web:60]

from custom_csv import CustomCsvWriter

rows = [
["name", "age", "comment"],
["Ram", 20, "hello, world"],
["Sita", 25, 'He said "Hi"'],
["Multi", 30, "line1\nline2"],
]

with open("output.csv", "w", newline="") as f:
writer = CustomCsvWriter(f)
writer.writerows(rows)


Behavior:

- If a field contains a comma, double quote, or newline, it is wrapped in double quotes. [web:42][web:60]
- Any existing `"` characters inside a field are escaped as `""` to keep the CSV valid. [web:64][web:65]
- The writer supports `writerow` for a single record and `writerows` for an iterable of records, similar to the standard `csv.writer` API. [web:22][web:73]

---

## 5. Benchmarking

The assignment requires benchmarking read and write performance against the built‑in `csv` module using a synthetic dataset. [web:77][web:83]

### 5.1 Generate benchmark data

First, create the synthetic CSV file that will be used for all benchmarks:

python generate_data.py


This script generates a file named `benchmark_data.csv` with a header row and at least 10,000 data rows, each containing 5 columns. Some fields intentionally contain commas, double quotes, and newline characters so that the benchmark also exercises edge‑case parsing and quoting behavior. [web:84][web:87]

### 5.2 Run the benchmark script

Next, run the benchmark that compares the custom implementation with Python’s built‑in `csv` module:

python benchmark.py


This script measures average execution time over multiple runs for four scenarios: reading with `csv.reader`, reading with `CustomCsvReader`, writing with `csv.writer`, and writing with `CustomCsvWriter`, using `time.perf_counter()` as a high‑resolution timer. [web:77][web:81][web:92]

Below is an example of how the results can be summarized (replace the sample numbers with your actual timings from running the script on your machine):

| Operation                      | Standard csv (s) | Custom parser (s) |
|-------------------------------|------------------|-------------------|
| Read `benchmark_data.csv`     | 0.12             | 0.35              |
| Write copy from rows in memory| 0.09             | 0.28              |

These results typically show that Python’s optimized `csv` module is faster, while the custom parser trades some performance for transparency and fine‑grained control over parsing rules. [web:80][web:83]

---

## 6. Design Choices and Limitations

- **State‑machine reader:** The reader follows a simple state‑machine design, tracking whether it is inside or outside a quoted field and interpreting commas, quotes, and newlines accordingly. This mirrors the behavior described for RFC‑style CSV files and common tooling. [web:43][web:55]
- **Streaming processing:** The reader works row by row without loading the entire file into memory, which is important when dealing with large CSVs in data‑engineering pipelines. [web:22]
- **Quoting and escaping rules:** The writer always escapes internal quotes by doubling them and adds surrounding quotes to fields that contain commas, quotes, or newlines, following widely used CSV conventions. [web:42][web:64][web:65]

This implementation focuses on common, well‑formed CSV data and the edge cases required by the assignment. It does not attempt to implement every variation of the CSV “standard” or recover from severely malformed input, but it provides a clear, educational example of how a CSV reader and writer can be built from first principles in Python. [web:22][web:43]



