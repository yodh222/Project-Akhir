"""
Modul Compress.

Modul ini menyediakan GUI dan logika utama untuk
melakukan kompresi file maupun folder menggunakan library gzip.
Folder akan dikemas terlebih dahulu ke dalam format TAR sebelum
dikompresi.
"""

import customtkinter as ctk
from tkinter import filedialog
import gzip
import tarfile
import os
import threading
from Helper.logCreate import LogCreate


class Compress(ctk.CTkFrame):
    """
    Kelas ini bertanggung jawab untuk menangani proses kompresi file
    atau folder berdasarkan pilihan pengguna melalui GUI, serta
    mencatat setiap proses ke dalam sistem log aplikasi.
    """

    def __init__(self, parent):
        """
        Mengatur tata letak antarmuka, input sumber dan output,
        serta tombol untuk memulai proses kompresi.
        """
        super().__init__(parent)
        self.pack(fill="both", expand=True, padx=40, pady=40)

        # Konfigurasi grid layout agar responsif
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_rowconfigure(10, weight=1)

        # SWITCH FILE / FOLDER
        ctk.CTkLabel(self, text="Switch Folder/File", font=("Arial", 15, "bold")).grid(
            row=0, column=0, sticky="w", pady=(0, 5)
        )
        self.combo_switch = ctk.CTkComboBox(self, values=["File", "Folder"])
        self.combo_switch.grid(row=1, column=0, sticky="ew", padx=(0, 10), pady=5)

        # SOURCE INPUT
        ctk.CTkLabel(self, text="Source File", font=("Arial", 15, "bold")).grid(
            row=2, column=0, sticky="w", pady=(0, 5)
        )
        self.entry_source = ctk.CTkEntry(self, placeholder_text="Select source")
        self.entry_source.grid(row=3, column=0, sticky="ew", padx=(0, 10), pady=5)
        ctk.CTkButton(
            self,
            text="Browse Source",
            width=140,
            command=self.browse_source
        ).grid(row=3, column=1, sticky="w", pady=5)

        # OUTPUT INPUT
        ctk.CTkLabel(self, text="Output Folder", font=("Arial", 15, "bold")).grid(
            row=4, column=0, sticky="w", pady=(20, 5)
        )
        self.entry_output = ctk.CTkEntry(self, placeholder_text="Select output folder")
        self.entry_output.grid(row=5, column=0, sticky="ew", padx=(0, 10), pady=5)
        ctk.CTkButton(
            self,
            text="Browse Output",
            width=140,
            command=self.browse_output
        ).grid(row=5, column=1, sticky="w", pady=5)

        # Tombol utama untuk memulai proses kompresi
        ctk.CTkButton(
            self,
            text="Start Compression",
            width=160,
            command=self.start_compression
        ).grid(row=10, column=0, columnspan=2, pady=40)

    # BROWSE METHODS

    def browse_source(self):
        """
        Membuka dialog pemilihan file atau folder sebagai sumber
        berdasarkan mode yang dipilih pengguna.
        """
        path = (
            filedialog.askopenfilename()
            if self.combo_switch.get() == "File"
            else filedialog.askdirectory()
        )

        if path:
            self.entry_source.delete(0, "end")
            self.entry_source.insert(0, path)

    def browse_output(self):
        """
        Membuka dialog pemilihan folder tujuan untuk hasil kompresi.
        """
        path = filedialog.askdirectory()
        if path:
            self.entry_output.delete(0, "end")
            self.entry_output.insert(0, path)

    # POPUP WINDOWS

    def show_wait_popup(self):
        """
        Menampilkan popup informasi bahwa proses kompresi sedang berjalan.
        Popup ini bersifat non-interaktif untuk mencegah gangguan proses.
        """
        self.popup = ctk.CTkToplevel(self)
        self.popup.title("Please Wait")
        self.popup.geometry("300x120")
        self.popup.resizable(False, False)

        ctk.CTkLabel(
            self.popup,
            text="Compressing...\nPlease wait.",
            font=("Arial", 16)
        ).pack(pady=20)

        # Mencegah popup ditutup saat proses berjalan
        self.popup.protocol("WM_DELETE_WINDOW", lambda: None)

    def show_finish_popup(self):
        """
        Menampilkan popup ketika proses kompresi berhasil diselesaikan.
        """
        if hasattr(self, "popup"):
            self.popup.destroy()

        done = ctk.CTkToplevel(self)
        done.title("Finished")
        done.geometry("300x120")

        ctk.CTkLabel(done, text="Compression Finished!", font=("Arial", 16)).pack(pady=20)
        ctk.CTkButton(done, text="OK", command=done.destroy).pack(pady=10)

    def show_error_popup(self, error):
        """
        Menampilkan popup kesalahan apabila terjadi error
        selama proses kompresi.
        """
        if hasattr(self, "popup"):
            self.popup.destroy()

        err = ctk.CTkToplevel(self)
        err.title("Error")
        err.geometry("300x150")

        ctk.CTkLabel(err, text="Error occurred!", font=("Arial", 16)).pack(pady=10)
        ctk.CTkLabel(err, text=error, wraplength=250).pack(pady=10)
        ctk.CTkButton(err, text="OK", command=err.destroy).pack(pady=10)

    # MAIN COMPRESSION LOGIC

    def compress_file(self, source, output):
        """
        Mengompresi satu file menggunakan algoritma gzip.

        File hasil kompresi akan disimpan dalam format .gz
        pada folder output yang ditentukan.
        """
        filename = os.path.basename(source)
        dest = os.path.join(output, filename + ".gz")

        LogCreate("CompressModule", f"Compressing file: {source} → {dest}")

        # Membaca file sumber dan menuliskannya ke file gzip
        with gzip.open(dest, "wb", compresslevel=9) as gz_out:
            with open(source, "rb") as src:
                gz_out.write(src.read())

        LogCreate("CompressModule", f"File compression completed: {dest}")

    def compress_folder(self, source, output):
        """
        Mengompresi folder dengan dua tahap, yaitu:
        1. Mengarsipkan folder ke format TAR
        2. Mengompresi hasil TAR ke format GZ

        Pendekatan ini digunakan untuk menjaga struktur folder.
        """
        folder_name = os.path.basename(source)
        tar_path = os.path.join(output, folder_name + ".tar")
        gz_path = tar_path + ".gz"

        LogCreate("CompressModule", f"Creating TAR archive: {tar_path}")

        # Tahap pertama: membuat arsip TAR
        with tarfile.open(tar_path, "w") as tar:
            tar.add(source, arcname=folder_name)

        LogCreate("CompressModule", f"TAR created. Compressing to GZ: {gz_path}")

        # Tahap kedua: mengompresi TAR menjadi GZ
        with open(tar_path, "rb") as tar_file:
            with gzip.open(gz_path, "wb", compresslevel=9) as gz_out:
                gz_out.write(tar_file.read())

        # Menghapus file TAR sementara
        os.remove(tar_path)

        LogCreate(
            "CompressModule",
            f"Folder compression completed: {gz_path}",
            level="SUCCESS"
        )

    # THREAD PROCESS

    def compress_process(self):
        """
        Menjalankan proses kompresi berdasarkan input pengguna.

        Fungsi ini dipisahkan agar dapat dijalankan pada thread
        terpisah sehingga antarmuka tetap responsif.
        """
        source = self.entry_source.get()
        output = self.entry_output.get()
        mode = self.combo_switch.get()

        LogCreate(
            "CompressModule",
            f"Compression started. Mode={mode}, Source={source}, Output={output}"
        )

        try:
            if mode == "File":
                self.compress_file(source, output)
            else:
                self.compress_folder(source, output)

            LogCreate(
                "CompressModule",
                "Compression finished successfully",
                level="SUCCESS"
            )

            self.after(0, self.show_finish_popup)

        except Exception as e:
            LogCreate("CompressModule", f"Error: {str(e)}", level="ERROR")
            self.after(0, lambda: self.show_error_popup(str(e)))

    def start_compression(self):
        """
        Memulai proses kompresi dengan menjalankan thread baru
        untuk mencegah GUI menjadi tidak responsif.
        """
        self.show_wait_popup()
        threading.Thread(target=self.compress_process).start()
