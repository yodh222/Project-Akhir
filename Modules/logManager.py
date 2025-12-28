"""
Modul LogManager.

Modul ini menyediakan fitur untuk melihat file log aplikasi
dalam format .log maupun .gz, serta melakukan kompresi otomatis
terhadap file log secara periodik menggunakan modul gzip.
"""

import customtkinter as ctk
from pathlib import Path
import gzip
import os
import threading
import time
import traceback
from datetime import datetime


class LogManager(ctk.CTkFrame):
    """
    Kelas ini menangani tampilan log aplikasi, pembacaan file log,
    serta proses kompresi otomatis file log yang berjalan
    di background thread.
    """

    def __init__(self, parent):
        """
        Mengatur antarmuka pemilihan log, tombol kontrol
        kompresi otomatis, serta fitur penampil isi log.
        """
        super().__init__(parent)
        self.pack(fill="both", expand=True, padx=40, pady=40)

        # Status kompresi otomatis
        self.compression_running = False
        self.compression_thread = None

        # GRID SETUP
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_rowconfigure(10, weight=1)

        # SOURCE LOG SELECTION
        ctk.CTkLabel(self, text="Choose Log File", font=("Arial", 15, "bold")).grid(
            row=0, column=0, sticky="w", pady=(0, 5)
        )
        self.log_switch = ctk.CTkComboBox(self, values=self.getLogs())
        self.log_switch.grid(
            row=1, column=0, sticky="ew", padx=(0, 10), pady=5, columnspan=4
        )

        # BUTTONS
        self.compress_btn = ctk.CTkButton(
            self,
            text="Start Auto Compression",
            width=160,
            command=self.toggle_auto_compression
        )
        self.compress_btn.grid(
            row=10, column=0, columnspan=2, sticky="e", padx=50
        )

        ctk.CTkButton(
            self,
            text="View Log",
            width=160,
            command=self.viewLog
        ).grid(row=10, column=2, sticky="w", padx=50)

    # LOG FILE HANDLING

    def getLogs(self):
        """
        Mengambil daftar file log dari folder Logs.

        Jika folder atau file log utama belum tersedia,
        maka akan dibuat secara otomatis.
        """
        log_dir = Path("Logs")
        log_dir.mkdir(parents=True, exist_ok=True)

        app_log = log_dir / "app.log"
        if not app_log.exists():
            app_log.touch()

        return [
            str(file.resolve())
            for file in log_dir.iterdir()
            if file.is_file()
        ]

    def viewLog(self):
        """
        Menampilkan isi file log yang dipilih pengguna.
        Mendukung file log biasa (.log) dan terkompresi (.gz).
        """
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
            error_msg = (
                f"Failed to open log file:\n{e}\n\n{traceback.format_exc()}"
            )
            self.open_log_viewer("Error", error_msg)

    # FILE READER METHODS

    def read_log_file(self, path):
        """
        Membaca isi file log teks (.log) dan
        mengembalikannya sebagai string.
        """
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return f.read()

    def read_gz_file(self, path):
        """
        Membaca dan mendekompresi file log berformat .gz
        untuk ditampilkan dalam bentuk teks.
        """
        with gzip.open(path, "rb") as gz_file:
            raw_bytes = gz_file.read()
            return raw_bytes.decode("utf-8", errors="replace")

    def open_log_viewer(self, title: str, content: str):
        """
        Menampilkan isi log dalam jendela baru
        menggunakan komponen textbox read-only.
        """
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
        textbox.configure(state="disabled")

    # AUTO COMPRESSION CONTROL

    def toggle_auto_compression(self):
        """
        Mengaktifkan atau menghentikan proses
        kompresi otomatis file log.
        """
        if not self.compression_running:
            self.start_auto_compression()
        else:
            self.stop_auto_compression()

    def start_auto_compression(self):
        """
        Memulai thread kompresi otomatis
        yang berjalan di background.
        """
        self.compression_running = True
        self.compress_btn.configure(text="Stop Auto Compression")

        self.compression_thread = threading.Thread(
            target=self.compression_loop,
            daemon=True
        )
        self.compression_thread.start()

    def stop_auto_compression(self):
        """
        Menghentikan proses kompresi otomatis file log.
        """
        self.compression_running = False
        self.compress_btn.configure(text="Start Auto Compression")

    # LOG RETENTION POLICY

    def cleanup_old_compressed_logs(self, log_dir: Path, max_files: int = 2):
        """
        Menghapus file log terkompresi lama berdasarkan
        kebijakan retensi untuk membatasi jumlah file.
        """
        compressed_logs = list(log_dir.glob("app-*.log.gz"))
        if len(compressed_logs) <= max_files:
            return

        # Mengurutkan file berdasarkan waktu modifikasi (tertua terlebih dahulu)
        compressed_logs.sort(key=lambda f: f.stat().st_mtime)

        # Menghapus file log terlama
        for old_file in compressed_logs[:-max_files]:
            try:
                old_file.unlink()
            except Exception as e:
                print(f"Failed to delete {old_file}: {e}")

    # THREAD PROCESS

    def compression_loop(self):
        """
        Loop utama untuk melakukan kompresi file log
        secara otomatis dengan interval waktu tertentu.
        """
        log_path = Path("Logs/app.log")
        log_dir = log_path.parent

        while self.compression_running:
            try:
                if log_path.exists():
                    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
                    output_file = log_dir / f"app-{timestamp}.log.gz"

                    # Mengompresi file log utama
                    with open(log_path, "rb") as f_in:
                        with gzip.open(output_file, "wb") as f_out:
                            f_out.writelines(f_in)

                    # Menjaga jumlah file log terkompresi
                    self.cleanup_old_compressed_logs(log_dir, max_files=2)

            except Exception as e:
                print("Compression error:", e)

            # Menunggu 60 detik sebelum kompresi berikutnya
            time.sleep(60)
