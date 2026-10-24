# Ghost Data Audit Agent

An automated privacy auditing tool built for the HackerRank Orchestrate Hackathon. It scans enterprise data stores for lingering PII deletion requests while ignoring raw request datasets to prevent false positives.

## Structure
- `agent.py`: Core audit engine that evaluates PII retention and generates compliance steps.
- `ingestion.py`: Helper script for reading and parsing incoming datasets.
- `logger.py`: Internal logging module.
- `main.py`: Entry point pipeline that executes audit runs and generates output.
- `deletion_requests.csv` & `deletion_rules.csv`: Dataset input files for audit validation.
- `output.csv`: Standardized audit trace results containing final status and JSON remediation arrays.
- `requirements.txt`: Project dependencies.

## Requirements
- Python 3.8+ 
- Uses standard library modules (`csv`, `json`, `os`, `re`, `pathlib`). No external packages required.

## Execution
Run the pipeline from the project root:
```bash
python main.py
