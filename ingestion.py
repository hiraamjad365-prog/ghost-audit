import csv
import os
from pathlib import Path

def load_governance_rules(file_path):
    abs_path = os.path.abspath(file_path)
    data = []
    if not os.path.exists(abs_path):
        print(f"[ERROR] Rules file does not exist at {abs_path}")
        return data
    with open(abs_path, mode='r', encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        print(f"[DEBUG] Rules CSV Fieldnames: {reader.fieldnames}")
        for row in reader:
            data.append(row)
    print(f"[DEBUG] Successfully loaded {len(data)} rules.")
    return data

def load_deletion_requests(file_path):
    abs_path = os.path.abspath(file_path)
    data = []
    if not os.path.exists(abs_path):
        print(f"[ERROR] Requests file does not exist at {abs_path}")
        return data
    with open(abs_path, mode='r', encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        print(f"[DEBUG] Requests CSV Fieldnames: {reader.fieldnames}")
        for row in reader:
            data.append(row)
    print(f"[DEBUG] Successfully loaded {len(data)} requests.")
    return data

def scan_enterprise_vault(corpus_dir):
    system_records = {}
    path = Path(corpus_dir).resolve()
    if not path.exists():
        return system_records
        
    for file_path in path.rglob('*'):
        if file_path.is_file():
            try:
                with open(file_path, 'r', encoding='utf-8-sig', errors='ignore') as f:
                    system_records[str(file_path)] = f.read()
            except Exception as e:
                system_records[str(file_path)] = f"[Binary or unreadable record: {e}]"
    return system_records