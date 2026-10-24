import csv
import json
import os
from ingestion import load_governance_rules, load_deletion_requests, scan_enterprise_vault
from agent import audit_user_footprint
from logger import AuditLogger

def main():
    logger = AuditLogger("log.txt")
    logger.info("Starting Ghost Data Audit Engine...")
    
    dataset_dir = "../dataset"
    if not os.path.exists(dataset_dir):
        dataset_dir = "dataset"

    rules_path = os.path.join(dataset_dir, "deletion_rules.csv")
    requests_path = os.path.join(dataset_dir, "deletion_requests.csv")
    
    logger.info(f"Loading data from directory: {dataset_dir}")
    
    rules = load_governance_rules(rules_path)
    requests = load_deletion_requests(requests_path)
    system_records = scan_enterprise_vault(dataset_dir)
    
    logger.info(f"Loaded {len(rules)} governance rules and {len(requests)} deletion requests.")
    logger.trace(f"Scanned {len(system_records)} total records across dataset vault.")
    
    output_rows = []
    
    for idx, req in enumerate(requests, 1):
        # Extract case_id matching hackathon schema (fallback to request_id or case_id)
        case_id = req.get("case_id", req.get("request_id", f"case_{idx:03d}"))
        logger.info(f"Processing Request [{idx}/{len(requests)}]: ID {case_id}")
        
        result = audit_user_footprint(req, rules, system_records, logger)
        
        # Ensure steps_json is correctly serialized to a JSON string
        steps = result.get("remediation_steps", [])
        if isinstance(steps, list):
            steps_json_str = json.dumps(steps)
        else:
            steps_json_str = str(steps)

        output_rows.append({
            "case_id": case_id,
            "deletion_status": result.get("status", "INCOMPLETE"),
            "steps_json": steps_json_str
        })

    output_path = "output.csv"
    fields = ["case_id", "deletion_status", "steps_json"]
    
    with open(output_path, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(output_rows)
        
    logger.info(f"Pipeline complete! Output generated at {output_path}")

if __name__ == "__main__":
    main()