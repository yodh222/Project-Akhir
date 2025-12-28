"""
Helper configServer.

Helper ini menyediakan utilitas untuk menyalin file server receiver
ke lokasi yang dipilih pengguna. Fitur ini digunakan untuk membantu
pengaturan sisi server dalam proses transfer data.
"""

import shutil
from tkinter import filedialog
import customtkinter as ctk
import sys
import os


def get_resource_path(relative_path):
    """
    Fungsi ini mendukung eksekusi dalam mode development
    maupun saat aplikasi dikemas menggunakan PyInstaller.
    """
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)

    return os.path.join(os.path.abspath("."), relative_path)


def save_local_file():
    """
    Menyimpan file server receiver ke lokasi lokal yang dipilih pengguna.

    Fungsi ini digunakan untuk menyalin file serverReciever.py
    agar pengguna dapat menjalankan server penerima data
    secara terpisah.
    """
    source_file = get_resource_path("Assets/serverReciever.py")

    save_path = filedialog.asksaveasfilename(
        title="Simpan file",
        initialfile="serverReciever.py",
        defaultextension=".py",
        filetypes=[("Python", ".py"), ("Semua File", "*.*")]
    )

    if not save_path:
        return

    # Menyalin file server ke lokasi tujuan
    shutil.copyfile(source_file, save_path)

    # Menampilkan informasi bahwa file berhasil disimpan
    info_label.configure(text="File berhasil disimpan.")
