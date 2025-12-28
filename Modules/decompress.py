"""
Modul Decompress.

Modul ini menangani proses dekompresi file menggunakan modul gzip.
Mendukung dekompresi file tunggal (.gz) maupun arsip folder (.tar.gz)
yang sebelumnya dikompresi oleh modul Compress.
"""

import customtkinter as ctk
from tkinter import filedialog
import gzip
import tarfile
import os
import threading

# Import modul logging aplikasi
from Helper.logCreate import LogCreate


class Decompress(ctk.CTkFrame):
    """
    Kelas ini menyediakan antarmuka grafis dan logika utama
    untuk mengembalikan file atau folder terkompresi
    ke bentuk aslinya.
    """

    def __init__(self, parent):
        """
        Mengatur input sumber file terkompresi, folder tujuan,
        serta tombol untuk memulai proses dekompresi.
        """
        super().__init__(parent)
        self.pack(fill="both", expand=True, padx=40, pady=40)

        # GRID SETUP
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_rowconfigure(10, weight=1)

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

        # Tombol untuk memulai proses dekompresi
        ctk.CTkButton(
            self,
            text="Start Decompression",
            width=160,
            command=self.start_decompression
        ).grid(row=10, column=0, columnspan=2, pady=40)

    # BROWSE METHODS

    def browse_source(self):
        """
        Membuka dialog pemilihan file terkompresi (.gz atau .tar.gz)
        yang akan didekompresi.
        """
        path = filedialog.askopenfilename()
        if path:
            self.entry_source.delete(0, "end")
            self.entry_source.insert(0, path)

    def browse_output(self):
        """
        Membuka dialog pemilihan folder tujuan hasil dekompresi.
        """
        path = filedialog.askdirectory()
        if path:
            self.entry_output.delete(0, "end")
            self.entry_output.insert(0, path)

    # NOTIFICATION METHOD

    def show_wait_popup(self):
        """
        Menampilkan popup informasi bahwa proses dekompresi
        sedang berlangsung dan mencegah interaksi pengguna.
        """
        self.popup = ctk.CTkToplevel(self)
        self.popup.title("Please Wait")
        self.popup.geometry("300x120")
        self.popup.resizable(False, False)

        ctk.CTkLabel(
            self.popup,
            text="Decompressing...\nPlease wait.",
            font=("Arial", 16)
        ).pack(pady=20)

        # Mencegah popup ditutup selama proses berjalan
        self.popup.protocol("WM_DELETE_WINDOW", lambda: None)

    def show_finish_popup(self):
        """
        Menampilkan popup ketika proses dekompresi
        berhasil diselesaikan.
        """
        if hasattr(self, "popup"):
            self.popup.destroy()

        done = ctk.CTkToplevel(self)
        done.title("Finished")
        done.geometry("300x120")

        ctk.CTkLabel(done, text="Decompression Finished!", font=("Arial", 16)).pack(pady=20)
        ctk.CTkButton(done, text="OK", command=done.destroy).pack(pady=10)

    def show_error_popup(self, error):
        """
        Menampilkan popup kesalahan apabila terjadi error
        selama proses dekompresi.
        """
        if hasattr(self, "popup"):
            self.popup.destroy()

        err = ctk.CTkToplevel(self)
        err.title("Error")
        err.geometry("300x150")

        ctk.CTkLabel(err, text="Error occurred!", font=("Arial", 16)).pack(pady=10)
        ctk.CTkLabel(err, text=error, wraplength=250).pack(pady=10)
        ctk.CTkButton(err, text="OK", command=err.destroy).pack(pady=10)

    # MAIN DECOMPRESSION LOGIC

    def decompress_file(self, source, output):
        """
        Mendekompresi satu file berformat .gz
        dan mengembalikannya ke bentuk file asli.
        """
        filename = os.path.basename(source)
        dest = os.path.join(output, filename[:-3])

        LogCreate(
            "DecompressModule",
            f"Decompressing single file: {source} → {dest}"
        )

        # Membaca isi file gzip dan menuliskannya ke file output
        with gzip.open(source, "rb") as gz_in:
            with open(dest, "wb") as dest_file:
                dest_file.write(gz_in.read())

        LogCreate(
            "DecompressModule",
            f"File decompression completed: {dest}",
            level="SUCCESS"
        )

    def decompress_folder(self, source, output):
        """
        Mendekompresi arsip .tar.gz dan mengekstraknya
        menjadi folder pada direktori tujuan.
        """
        folder_name = os.path.basename(source)
        tar_path = os.path.join(output, folder_name[:-7])

        LogCreate(
            "DecompressModule",
            f"Extracting TAR.GZ: {source} → {tar_path}"
        )

        # Mengekstrak arsip TAR.GZ ke folder tujuan
        with tarfile.open(source, "r:gz") as tar:
            tar.extractall(path=tar_path)

        LogCreate(
            "DecompressModule",
            f"Folder extracted successfully: {tar_path}",
            level="SUCCESS"
        )

    # THREAD PROCESS

    def decompress_process(self):
        """
        Menentukan jenis file terkompresi dan menjalankan
        proses dekompresi yang sesuai pada thread terpisah.
        """
        source = self.entry_source.get()
        output = self.entry_output.get()

        LogCreate(
            "DecompressModule",
            f"Decompression started. Source={source}, Output={output}"
        )

        try:
            if source.endswith(".tar.gz"):
                LogCreate("DecompressModule", "Mode: TAR.GZ Folder Decompression")
                self.decompress_folder(source, output)
            else:
                LogCreate("DecompressModule", "Mode: Single .GZ File Decompression")
                self.decompress_file(source, output)

            LogCreate(
                "DecompressModule",
                "Decompression finished successfully",
                level="SUCCESS"
            )

            self.after(0, self.show_finish_popup)

        except Exception as e:
            LogCreate("DecompressModule", f"Error: {str(e)}", level="ERROR")
            self.after(0, lambda: self.show_error_popup(str(e)))

    def start_decompression(self):
        """
        Memulai proses dekompresi dengan menjalankan
        thread baru agar antarmuka tetap responsif.
        """
        self.show_wait_popup()
        threading.Thread(target=self.decompress_process).start()
