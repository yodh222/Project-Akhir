"""
File utama (entry point) aplikasi Project Algoritma dan Pemrograman.

Aplikasi ini menggunakan CustomTkinter untuk membangun antarmuka grafis
yang menyediakan fitur kompresi file, dekompresi file, transfer data,
serta manajemen dan otomatisasi kompresi file log.

Setiap fitur diimplementasikan dalam modul terpisah untuk menerapkan
konsep modularisasi dan pemisahan tanggung jawab program.
"""

import customtkinter as ctk
from Modules.compress import Compress
from Modules.decompress import Decompress
from Modules.transferData import TransferData
from Modules.logManager import LogManager


# Root window utama aplikasi
SCREEN_ROOT = ctk.CTk()

# Frame menu navigasi di bagian atas
MENU = ctk.CTkFrame(SCREEN_ROOT, fg_color="#1e1e1e", height=50)

# Frame utama untuk menampilkan halaman fitur
FRAME = ctk.CTkFrame(SCREEN_ROOT)


def menuHandler(PageClass):
    """
    Menangani perpindahan halaman antar fitur aplikasi.

    Fungsi ini akan menghapus frame halaman sebelumnya dan
    menampilkan frame baru berdasarkan kelas halaman yang dipilih
    melalui menu navigasi.
    """
    global FRAME

    # Menghapus frame lama untuk mencegah tumpang tindih tampilan
    if FRAME is not None:
        FRAME.destroy()

    # Membuat frame baru dan memuat halaman sesuai menu yang dipilih
    FRAME = ctk.CTkFrame(SCREEN_ROOT)
    PageClass(FRAME)
    FRAME.pack(fill="both", expand=True)


def setupMenu():
    """
    Mengatur dan menampilkan menu navigasi utama aplikasi.

    Menu ini memungkinkan pengguna berpindah antar fitur:
    Compress, Decompress, Transfer Data, dan Log Manager.
    """
    MENU.pack(side="top", fill="x")

    # Tombol menu untuk halaman kompresi file
    ctk.CTkButton(
        MENU,
        text="Compress",
        width=120,
        fg_color="#1e1e1e",
        hover_color="#333333",
        command=lambda: menuHandler(Compress)
    ).pack(side="left", padx=5, pady=5)

    # Tombol menu untuk halaman dekompresi file
    ctk.CTkButton(
        MENU,
        text="Decompress",
        width=120,
        fg_color="#1e1e1e",
        hover_color="#333333",
        command=lambda: menuHandler(Decompress)
    ).pack(side="left", padx=5, pady=5)

    # Tombol menu untuk halaman transfer data ke server
    ctk.CTkButton(
        MENU,
        text="Transfer Data",
        width=120,
        fg_color="#1e1e1e",
        hover_color="#333333",
        command=lambda: menuHandler(TransferData)
    ).pack(side="left", padx=5, pady=5)

    # Tombol menu untuk halaman manajemen dan kompresi log
    ctk.CTkButton(
        MENU,
        text="Log Manager",
        width=120,
        fg_color="#1e1e1e",
        hover_color="#333333",
        command=lambda: menuHandler(LogManager)
    ).pack(side="left", padx=5, pady=5)

    # Menampilkan halaman kompresi sebagai halaman awal
    menuHandler(Compress)


def main():
    """
    Fungsi utama untuk menjalankan aplikasi.

    Fungsi ini bertanggung jawab untuk mengatur tampilan awal,
    memuat menu navigasi, serta menjalankan event loop GUI.
    """
    # Mengatur tema tampilan aplikasi
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    # Konfigurasi ukuran dan judul window utama
    SCREEN_ROOT.geometry("900x500")
    SCREEN_ROOT.title("Project Algoritma dan Pemrograman")

    # Inisialisasi menu dan menjalankan aplikasi
    setupMenu()
    SCREEN_ROOT.mainloop()


# Menjalankan aplikasi jika file ini dieksekusi langsung
if __name__ == "__main__":
    main()
