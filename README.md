# Custom CSV Parser in Python

This project implements a custom CSV reader and writer from scratch in Python
to understand how CSV parsing and serialization work internally.

More details about usage, design, and benchmarks will be added later.

## Benchmark summary

The script `generate_data.py` creates a `benchmark_data.csv` file with 10,000+ rows.
The script `benchmark.py` measures average read/write time for both the custom parser
and Python's built-in `csv` module using `time.perf_counter()` over multiple runs. [web:22][web:81][web:92]
