"""
Module: Custom Audit Logger for Ghost Data Agent
Author: Hira Amjad
Description: Dual-stream logging for real-time terminal feedback and log.txt generation.
"""

import datetime
import os

class AuditLogger:
    def __init__(self, log_filename="log.txt"):
        self.log_filename = log_filename
        with open(self.log_filename, "w", encoding="utf-8") as f:
            f.write(f"==================================================\n")
            f.write(f"NORTHSTAR SHOP - GHOST DATA AUDIT EXECUTION LOG\n")
            f.write(f"Timestamp: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"==================================================\n\n")

    def info(self, message):
        self._write_log("INFO", message)

    def trace(self, message):
        self._write_log("TRACE", message)

    def warning(self, message):
        self._write_log("WARNING", message)

    def error(self, message):
        self._write_log("ERROR", message)

    def _write_log(self, level, message):
        timestamp = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
        log_entry = f"[{timestamp}] [{level}] {message}"
        print(log_entry)
        with open(self.log_filename, "a", encoding="utf-8") as f:
            f.write(log_entry + "\n")