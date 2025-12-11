import customtkinter as ctk
from tkinter import filedialog
import Helper.configServer as cs
import socket
import os
import gzip
import shutil
import tempfile

class TransferData(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill="both", expand=True, padx=40, pady=40) 
        
        # GRID SETUP
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_rowconfigure(10, weight=1)

        # IP Target
        ctk.CTkLabel(
            self, text="IP Target",
            font=("Arial", 15, "bold"),
            anchor="w"
        ).grid(row=0, column=0, sticky="w", pady=(0, 5))

        self.entry_ip = ctk.CTkEntry(self, placeholder_text="Please Enter IP Target (i.e. 192.168.1.1)")
        self.entry_ip.grid(row=1, column=0, columnspan=4, sticky="ew", padx=(0,10), pady=5)

        # Port
        ctk.CTkLabel(
            self, text="Port",
            font=("Arial", 15, "bold"),
            anchor="w"
        ).grid(row=4, column=0, sticky="w", pady=(20, 5))

        self.entry_port = ctk.CTkEntry(self, placeholder_text="Please Enter Port (i.e. 22)")
        self.entry_port.grid(row=5, column=0, columnspan=4, sticky="ew", padx=(0,10), pady=5)

        # File to be Transfer
        ctk.CTkLabel(
            self, text="File to be Transfer",
            font=("Arial", 15, "bold"),
            anchor="w"
        ).grid(row=6, column=0, sticky="w", pady=(20, 5))

        self.entry_file = ctk.CTkEntry(self, placeholder_text="Select File")
        self.entry_file.grid(row=7, column=0, columnspan=3, sticky="ew", padx=(0,10), pady=5)

        ctk.CTkButton(self, text="Browse File", width=140, command=self.search_file).grid(
            row=7, column=3, sticky="ew", pady=5
        )

        # Buttons
        ctk.CTkButton(self, text="Send Data", width=160, command=self.sendData).grid(
            row=10, column=0, columnspan=2, pady=20
        )

        ctk.CTkButton(self, text="Save Server Reciever", width=160, command=cs.save_local_file).grid(
            row=10, column=2, columnspan=2, pady=20
        )

    # FILE BROWSER
    def search_file(self):
        path = filedialog.askopenfilename()
        if path:
            self.entry_file.delete(0, "end")
            self.entry_file.insert(0, path)
    
    def show_processing_window(self):
        self.win_processing = ctk.CTkToplevel(self)
        self.win_processing.title("Processing")
        self.win_processing.geometry("300x120")
        self.win_processing.resizable(False, False)

        ctk.CTkLabel(
            self.win_processing,
            text="Mengirim data...\nHarap tunggu...",
            font=("Arial", 14)
        ).pack(pady=20)

        # Pastikan popup selalu di atas
        self.win_processing.attributes("-topmost", True)

    def show_success_window(self):
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
            win_success, text="OK", width=100, command=win_success.destroy
        ).pack()
    
    def show_error_window(self, message):
        win_error = ctk.CTkToplevel(self)
        win_error.title("Error")
        win_error.geometry("350x150")
        win_error.resizable(False, False)

        ctk.CTkLabel(
            win_error,
            text="Terjadi Kesalahan:",
            font=("Arial", 16, "bold"),
            text_color="red"
        ).pack(pady=(20,5))

        ctk.CTkLabel(
            win_error,
            text=message,
            font=("Arial", 14),
            wraplength=300,
            justify="center"
        ).pack(pady=5)

        ctk.CTkButton(
            win_error, text="OK", width=100, command=win_error.destroy
        ).pack(pady=(10, 15))

        win_error.attributes("-topmost", True)

    # SEND DATA METHOD
    def sendData(self):
        HOST = self.entry_ip.get().strip()
        PORT = self.entry_port.get().strip()
        FILEPATH = self.entry_file.get().strip()

        # Validasi
        if not HOST or not PORT or not FILEPATH:
            self.show_error_window("IP, Port, dan File wajib diisi!")
            return
        
        if not os.path.exists(FILEPATH):
            self.show_error_window("File tidak ditemukan!")
            return

        try:
            PORT = int(PORT)
        except:
            self.show_error_window("Port harus berupa angka!")
            return

        # Tampilkan popup processing
        self.show_processing_window()
        self.update()

        # CEK APAKAH FILE SUDAH GZIP (.gz)
        if FILEPATH.lower().endswith(".gz"):
            file_to_send = FILEPATH
            nama_file = os.path.basename(FILEPATH)

        else:
            temp_dir = tempfile.gettempdir()
            nama_file = os.path.basename(FILEPATH) + ".gz"
            file_to_send = os.path.join(temp_dir, nama_file)

            try:
                with open(FILEPATH, "rb") as src, gzip.open(file_to_send, "wb") as dst:
                    shutil.copyfileobj(src, dst)
            except Exception as e:
                self.win_processing.destroy()
                self.show_error_window(f"Gagal mengkompres file:\n{e}")
                return

        # MULAI PROSES PENGIRIMAN
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((HOST, PORT))

            s.sendall((nama_file + "\n").encode("utf-8"))

            with open(file_to_send, "rb") as f:
                while True:
                    chunk = f.read(1024)
                    if not chunk:
                        break
                    s.sendall(chunk)

            print("Pengiriman selesai")

            # Tutup processing window
            if hasattr(self, "win_processing"):
                self.win_processing.destroy()

            # Tampilkan Success Window
            self.show_success_window()

        except Exception as e:
            if hasattr(self, "win_processing"):
                self.win_processing.destroy()

            # Tampilkan Error Window
            self.show_error_window(f"Gagal mengirim data:\n{e}")

        finally:
            try:
                s.close()
            except:
                pass