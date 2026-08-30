# GGUF Seed Fuzzer

A minimal, spec-compliant GGUF file generator for fuzzing research, 
paired with a pytest test suite covering both valid parsing and 
error handling.

## What it does

Manually constructs a GGUF file header byte by byte, strictly following 
the binary specification (field order, field size, endianness). This 
produces a minimal valid "seed" file — the kind of input fuzzing tools 
like AFL mutate to search for crashes in GGUF parsers.

## Test coverage

The test suite (10 tests) validates:
- Correct byte-level encoding of the header (magic number, version, 
  tensor/metadata counts)
- Round-trip parsing of a valid header
- Graceful error handling for malformed input (empty file, wrong magic 
  number, truncated header) — raising clear `ValueError`s instead of 
  cryptic low-level struct errors

## Usage

\```bash
pip install -r requirements.txt
python create_mini_seed.py      # generates mini_seed.gguf
pytest test_create_mini_seed.py -v
\```

## Running tests with Docker

```bash
docker build -t gguf-seed-fuzzer .
docker run gguf-seed-fuzzer
```
