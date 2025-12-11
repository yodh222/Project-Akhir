from datetime import datetime
import os

class LogCreate:
    def __init__(self, process_name="UnknownProcess", detail="", level="INFO"):
        self.log_path = "Logs/app.log"

        # Pastikan folder Log ada
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)

        # Format timestamp
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Format final log sesuai kebutuhan
        log_line = f"[{timestamp}] [{level}] {process_name} - {detail}\n"

        # Tulis ke file .log
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(log_line)
