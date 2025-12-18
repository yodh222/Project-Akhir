from ctypes import Array
import customtkinter as ctk
from pathlib import Path
import traceback
import gzip
import io
import os
import traceback
import threading
import time
from datetime import datetime


class LogManager(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill="both", expand=True, padx=40, pady=40)
        
        self.compression_running = False
        self.compression_thread = None

        # GRID SETUP
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_rowconfigure(10, weight=1)

        # Source Log
        ctk.CTkLabel(self, text="Choose Log File", font=("Arial", 15, "bold")).grid(
            row=0, column=0, sticky="w", pady=(0, 5)
        )
        self.log_switch = ctk.CTkComboBox(self, values=self.getLogs())
        self.log_switch.grid(row=1, column=0, sticky="ew", padx=(0, 10), pady=5, columnspan=4)
        
        # Button
        self.compress_btn = ctk.CTkButton(self, text="Start Auto Compression", width=160,  command=self.toggle_auto_compression)
        self.compress_btn.grid(
            row=10, column=0, columnspan=2, sticky="e", padx=50
        )
        ctk.CTkButton(self, text="View Log", width=160, command=self.viewLog).grid(
            row=10, column=2, columnspan=1, sticky="w", padx=50
        )
    def getLogs(self):
        log_dir = Path("Logs")
        return [str(file.resolve()) for file in log_dir.iterdir() if file.is_file()]
    
    def viewLog(self):
        selected_log = self.log_switch.get()

        if not selected_log:
            return

        try:
            ext = Path(selected_log).suffix.lower()

            if ext == ".log":
                content = self.read_log_file(selected_log)

            elif ext == ".gz":
                content = self.read_gz_file(selected_log)

            else:
                content = f"Unsupported file type: {ext}"

            self.open_log_viewer(selected_log, content)

        except Exception as e:
            error_msg = f"Failed to open log file:\n{e}\n\n{traceback.format_exc()}"
            self.open_log_viewer("Error", error_msg)
    
    # Main Processs
    def read_log_file(self, path):
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return f.read()
    def read_gz_file(self, path):
        with gzip.open(path, "rb") as gz_file:
            raw_bytes = gz_file.read()
            return raw_bytes.decode("utf-8", errors="replace")
    
    def open_log_viewer(self, title: str, content: str):
        viewer = ctk.CTkToplevel(self)
        viewer.title(f"Log Viewer - {os.path.basename(title)}")
        viewer.geometry("900x600")
        viewer.grid_rowconfigure(0, weight=1)
        viewer.grid_columnconfigure(0, weight=1)

        textbox = ctk.CTkTextbox(
            viewer,
            wrap="none",
            font=("Consolas", 12)
        )
        textbox.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        textbox.insert("1.0", content)
        textbox.configure(state="disabled")  # read-only

    # Auto Compress
    def toggle_auto_compression(self):
        if not self.compression_running:
            self.start_auto_compression()
        else:
            self.stop_auto_compression()

    def start_auto_compression(self):
        self.compression_running = True
        self.compress_btn.configure(text="Stop Auto Compression")

        self.compression_thread = threading.Thread(
            target=self.compression_loop,
            daemon=True
        )
        self.compression_thread.start()

    def stop_auto_compression(self):
        self.compression_running = False
        self.compress_btn.configure(text="Start Auto Compression")

    def cleanup_old_compressed_logs(self, log_dir: Path, max_files: int = 2):
        compressed_logs = list(log_dir.glob("app-*.log.gz"))

        if len(compressed_logs) <= max_files:
            return

        # Sort berdasarkan waktu modifikasi (paling lama dulu)
        compressed_logs.sort(key=lambda f: f.stat().st_mtime)

        # Hapus file paling lama
        for old_file in compressed_logs[:-max_files]:
            try:
                old_file.unlink()
            except Exception as e:
                print(f"Failed to delete {old_file}: {e}")
    
    def compression_loop(self):
        log_path = Path("Logs/app.log")
        log_dir = log_path.parent

        while self.compression_running:
            try:
                if log_path.exists():
                    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
                    output_file = log_dir / f"app-{timestamp}.log.gz"

                    with open(log_path, "rb") as f_in:
                        with gzip.open(output_file, "wb") as f_out:
                            f_out.writelines(f_in)

                    # 🔥 retention policy: maksimal 2 file
                    self.cleanup_old_compressed_logs(log_dir, max_files=2)

            except Exception as e:
                print("Compression error:", e)

            time.sleep(60)