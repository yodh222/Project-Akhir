import shutil
from tkinter import filedialog
import customtkinter as ctk
import sys, os

def get_resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def save_local_file():
    source_file = get_resource_path("Assets/serverReciever.py")

    save_path = filedialog.asksaveasfilename(
        title="Simpan file",
        initialfile="serverReciever.py",
        defaultextension=".py",
        filetypes=[("Python", ".py"), ("Semua File", "*.*")]
    )

    if not save_path:
        return

    shutil.copyfile(source_file, save_path)
    info_label.configure(text="File berhasil disimpan.")
