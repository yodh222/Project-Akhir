"""
Helper LogCreate.

Helper ini digunakan untuk mencatat aktivitas aplikasi ke dalam
file log dengan format timestamp, level log, nama proses,
dan detail pesan.

Log disimpan dalam file app.log di dalam folder Logs.
"""

from datetime import datetime
import os


class LogCreate:
    """
    Kelas ini berfungsi sebagai utilitas logging sederhana
    untuk mencatat proses yang terjadi pada setiap modul
    aplikasi.
    """

    def __init__(self, process_name="UnknownProcess", detail="", level="INFO"):
        """
        Parameter:
        - process_name : nama modul atau proses yang mencatat log
        - detail       : deskripsi aktivitas atau pesan log
        - level        : tingkat log (INFO, SUCCESS, ERROR)
        """
        self.log_path = "Logs/app.log"

        # Memastikan folder Logs tersedia
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)

        # Membuat timestamp saat log dicatat
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Menyusun format log akhir
        log_line = f"[{timestamp}] [{level}] {process_name} - {detail}\n"

        # Menuliskan log ke file app.log (append mode)
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(log_line)
