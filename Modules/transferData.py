"""
Modul TransferData.

Modul ini menangani proses pengiriman file ke server tujuan
menggunakan socket TCP. File akan dikompresi terlebih dahulu
menggunakan gzip jika belum dalam format .gz untuk efisiensi
pengiriman data.
"""

import customtkinter as ctk
from tkinter import filedialog
import Helper.configServer as cs
import socket
import os
import gzip
import shutil
import tempfile
import threading

# Import modul logging aplikasi
from Helper.logCreate import LogCreate


class TransferData(ctk.CTkFrame):
    """
    Kelas ini menyediakan antarmuka grafis dan logika utama
    untuk mengirim file terkompresi ke server berdasarkan
    alamat IP dan port yang ditentukan pengguna.
    """

    def __init__(self, parent):
        """
        Mengatur input IP target, port server, pemilihan file,
        serta tombol untuk memulai proses pengiriman data.
        """
        super().__init__(parent)
        self.pack(fill="both", expand=True, padx=40, pady=40)

        # GRID SETUP
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_rowconfigure(10, weight=1)

        # IP TARGET INPUT
        ctk.CTkLabel(
            self,
            text="IP Target",
            font=("Arial", 15, "bold"),
            anchor="w"
        ).grid(row=0, column=0, sticky="w", pady=(0, 5))

        self.entry_ip = ctk.CTkEntry(
            self,
            placeholder_text="Please Enter IP Target (i.e. 192.168.1.1)"
        )
        self.entry_ip.grid(
            row=1, column=0, columnspan=4, sticky="ew", padx=(0, 10), pady=5
        )

        # PORT INPUT
        ctk.CTkLabel(
            self,
            text="Port",
            font=("Arial", 15, "bold"),
            anchor="w"
        ).grid(row=4, column=0, sticky="w", pady=(20, 5))

        self.entry_port = ctk.CTkEntry(
            self,
            placeholder_text="Please Enter Port (i.e. 22)"
        )
        self.entry_port.grid(
            row=5, column=0, columnspan=4, sticky="ew", padx=(0, 10), pady=5
        )

        # FILE SELECTION
        ctk.CTkLabel(
            self,
            text="File to be Transfer",
            font=("Arial", 15, "bold"),
            anchor="w"
        ).grid(row=6, column=0, sticky="w", pady=(20, 5))

        self.entry_file = ctk.CTkEntry(self, placeholder_text="Select File")
        self.entry_file.grid(
            row=7, column=0, columnspan=3, sticky="ew", padx=(0, 10), pady=5
        )

        ctk.CTkButton(
            self,
            text="Browse File",
            width=140,
            command=self.search_file
        ).grid(row=7, column=3, sticky="ew", pady=5)

        # ACTION BUTTONS
        ctk.CTkButton(
            self,
            text="Send Data",
            width=160,
            command=self.sendData
        ).grid(row=10, column=0, columnspan=2, pady=20)

        ctk.CTkButton(
            self,
            text="Save Server Reciever",
            width=160,
            command=cs.save_local_file
        ).grid(row=10, column=2, columnspan=2, pady=20)

    # FILE BROWSER

    def search_file(self):
        """
        Membuka dialog pemilihan file yang akan dikirim ke server.
        """
        path = filedialog.askopenfilename()
        if path:
            self.entry_file.delete(0, "end")
            self.entry_file.insert(0, path)

    # NOTIFICATION WINDOWS

    def show_processing_window(self):
        """
        Menampilkan popup informasi bahwa proses
        pengiriman data sedang berlangsung.
        """
        self.win_processing = ctk.CTkToplevel(self)
        self.win_processing.title("Processing")
        self.win_processing.geometry("300x120")
        self.win_processing.resizable(False, False)

        ctk.CTkLabel(
            self.win_processing,
            text="Mengirim data...\nHarap tunggu...",
            font=("Arial", 14)
        ).pack(pady=20)

        self.win_processing.attributes("-topmost", True)

    def show_success_window(self):
        """
        Menampilkan popup ketika proses pengiriman data
        berhasil diselesaikan.
        """
        win_success = ctk.CTkToplevel(self)
        win_success.title("Success")
        win_success.geometry("300x120")
        win_success.resizable(False, False)

        ctk.CTkLabel(
            win_success,
            text="Pengiriman selesai!",
            font=("Arial", 16, "bold")
        ).pack(pady=25)

        ctk.CTkButton(
            win_success,
            text="OK",
            width=100,
            command=win_success.destroy
        ).pack()

    def show_error_window(self, message):
        """
        Menampilkan popup kesalahan jika terjadi error
        selama proses validasi atau pengiriman data.
        """
        win_error = ctk.CTkToplevel(self)
        win_error.title("Error")
        win_error.geometry("350x150")
        win_error.resizable(False, False)

        ctk.CTkLabel(
            win_error,
            text="Terjadi Kesalahan:",
            font=("Arial", 16, "bold"),
            text_color="red"
        ).pack(pady=(20, 5))

        ctk.CTkLabel(
            win_error,
            text=message,
            font=("Arial", 14),
            wraplength=300,
            justify="center"
        ).pack(pady=5)

        ctk.CTkButton(
            win_error,
            text="OK",
            width=100,
            command=win_error.destroy
        ).pack(pady=(10, 15))

        win_error.attributes("-topmost", True)

    # SEND DATA PROCESS

    def sendData(self):
        """
        Menjalankan proses pengiriman data pada thread terpisah
        agar antarmuka tetap responsif.
        """
        threading.Thread(target=self.send_process).start()

    def send_process(self):
        """
        Proses utama pengiriman data yang mencakup:
        validasi input, kompresi file jika diperlukan,
        serta pengiriman data ke server melalui socket TCP.
        """
        HOST = self.entry_ip.get().strip()
        PORT = self.entry_port.get().strip()
        FILEPATH = self.entry_file.get().strip()

        LogCreate("TransferModule", "Initializing data transfer...")

        # VALIDATION
        if not HOST or not PORT or not FILEPATH:
            self.after(0, lambda: self.show_error_window("IP, Port, dan File wajib diisi!"))
            LogCreate(
                "TransferModule",
                "Validation failed: Missing IP/Port/File",
                level="ERROR"
            )
            return

        if not os.path.exists(FILEPATH):
            self.after(0, lambda: self.show_error_window("File tidak ditemukan!"))
            LogCreate(
                "TransferModule",
                f"File not found: {FILEPATH}",
                level="ERROR"
            )
            return

        try:
            PORT = int(PORT)
        except ValueError:
            self.after(0, lambda: self.show_error_window("Port harus berupa angka!"))
            LogCreate(
                "TransferModule",
                f"Invalid port number: {PORT}",
                level="ERROR"
            )
            return

        # Menampilkan popup proses di thread utama
        self.after(0, self.show_processing_window)

        # CHECK IF FILE ALREADY COMPRESSED
        if FILEPATH.lower().endswith(".gz"):
            LogCreate("TransferModule", f"File already compressed (.gz): {FILEPATH}")
            file_to_send = FILEPATH
            nama_file = os.path.basename(FILEPATH)
        else:
            LogCreate("TransferModule", f"Compressing file before sending: {FILEPATH}")
            temp_dir = tempfile.gettempdir()
            nama_file = os.path.basename(FILEPATH) + ".gz"
            file_to_send = os.path.join(temp_dir, nama_file)

            try:
                # Mengompresi file sementara sebelum dikirim
                with open(FILEPATH, "rb") as src, gzip.open(file_to_send, "wb") as dst:
                    shutil.copyfileobj(src, dst)

                LogCreate(
                    "TransferModule",
                    f"Temporary gz file created: {file_to_send}"
                )

            except Exception as e:
                self.after(
                    0,
                    lambda: self.show_error_window(f"Gagal mengkompres file:\n{e}")
                )
                LogCreate(
                    "TransferModule",
                    f"Compression failed: {e}",
                    level="ERROR"
                )
                return

        # BEGIN TRANSFER PROCESS
        try:
            LogCreate("TransferModule", f"Connecting to {HOST}:{PORT}")

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((HOST, PORT))

            LogCreate(
                "TransferModule",
                f"Connected to server. Sending filename: {nama_file}"
            )

            # Mengirim nama file terlebih dahulu
            s.sendall((nama_file + "\n").encode("utf-8"))

            total_sent = 0
            file_size = os.path.getsize(file_to_send)

            # Mengirim file dalam bentuk potongan data (chunk)
            with open(file_to_send, "rb") as f:
                while True:
                    chunk = f.read(1024)
                    if not chunk:
                        break

                    s.sendall(chunk)
                    total_sent += len(chunk)

            LogCreate(
                "TransferModule",
                f"Transfer completed. Bytes sent: {total_sent}/{file_size}",
                level="SUCCESS"
            )

            # Menutup popup proses dan menampilkan notifikasi sukses
            self.after(0, lambda: self.win_processing.destroy())
            self.after(0, self.show_success_window)

        except Exception as e:
            LogCreate("TransferModule", f"Transfer failed: {e}", level="ERROR")
            self.after(0, lambda: self.win_processing.destroy())
            self.after(
                0,
                lambda: self.show_error_window(f"Gagal mengirim data:\n{e}")
            )

        finally:
            try:
                s.close()
                LogCreate("TransferModule", "Socket closed")
            except Exception:
                LogCreate(
                    "TransferModule",
                    "Socket failed to close",
                    level="ERROR"
                )
