import re
import json

def audit_user_footprint(request, rules, system_records, logger=None):
    user_email = request.get("email", "").strip().lower()
    user_id = request.get("user_id", "").strip()
    
    # Check reported status or request flags
    reported_status = request.get("reported_status", "").strip().upper()
    
    exposed_records = []
    recreation_paths = []
    steps = []
    
    step_counter = 1

    # Step 1: FINDING phase - scan enterprise vault (excluding raw source CSVs)
    for file_path, content in system_records.items():
        # Skip source datasets/rules files so we don't false-positive match the request itself
        if "deletion_requests.csv" in file_path or "deletion_rules.csv" in file_path or "sample" in file_path:
            continue
            
        content_lower = content.lower()
        found_email = user_email and user_email in content_lower
        found_id = user_id and user_id in content

        if found_email or found_id:
            exposed_records.append(file_path)
            steps.append({
                "step_no": step_counter,
                "phase": "FINDING",
                "system_id": file_path,
                "operation": "DETECT_PII",
                "details": f"Lingering user identifier found in {file_path}"
            })
            step_counter += 1
            
            if any(k in file_path.lower() for k in ["backup", "sync", "export", "archive", "log", "restore"]):
                recreation_paths.append(f"Potential sync re-creation vector in {file_path}")

    # Determine status based on findings and reported status
    if exposed_records:
        status = "INCOMPLETE"
        steps.append({
            "step_no": step_counter,
            "phase": "REMEDIATION",
            "system_id": "MULTIPLE",
            "operation": "PURGE_DATA",
            "details": f"Purge/anonymize lingering user identifiers across {len(exposed_records)} identified records."
        })
        step_counter += 1
        
        remediation_text = (
            f"1. Purge/anonymize lingering user identifiers across {len(exposed_records)} identified records. "
            f"2. Audit and update active sync scripts to prevent automatic data re-creation."
        )
        if logger:
            logger.warning(f"Lingering data detected across {len(exposed_records)} location(s). Marked INCOMPLETE.")
    else:
        status = "COMPLETE" if reported_status != "NOT_STARTED" else "PARTIALLY_COMPLETE"
        steps.append({
            "step_no": step_counter,
            "phase": "VERIFICATION",
            "system_id": "VAULT",
            "operation": "CONFIRM_DELETION",
            "details": "Audit passed: No lingering identifiers detected across secondary systems or logs."
        })
        remediation_text = "Audit passed: No lingering identifiers detected across secondary systems, search indexes, or logs."
        if logger:
            logger.info("No lingering data found. Marked COMPLETE.")

    return {
        "status": status,
        "exposed_records": "; ".join(exposed_records) if exposed_records else "None",
        "active_recreation_paths": "; ".join(recreation_paths) if recreation_paths else "None",
        "remediation_steps": steps  # Return as list, main.py will handle json.dumps
    }