import customtkinter as ctk
from Modules.compress import Compress
from Modules.decompress import Decompress
from Modules.transferData import TransferData
from Modules.logManager import LogManager

SCREEN_ROOT = ctk.CTk()
MENU = ctk.CTkFrame(SCREEN_ROOT, fg_color="#1e1e1e", height=50)
FRAME = ctk.CTkFrame(SCREEN_ROOT)

# MENANGANI PERGANTIAN HALAMAN
def menuHandler(PageClass):
    global FRAME

    # Hapus frame lama jika ada
    if FRAME is not None:
        FRAME.destroy()

    # Buat frame baru
    FRAME = ctk.CTkFrame(SCREEN_ROOT)
    PageClass(FRAME)
    FRAME.pack(fill="both", expand=True)


# Setup Menu
def setupMenu():
    MENU.pack(side="top", fill="x")

    ctk.CTkButton(MENU, text="Compress", width=120, fg_color="#1e1e1e",
                hover_color="#333333", command=lambda: menuHandler(Compress)).pack(side="left", padx=5, pady=5)

    ctk.CTkButton(MENU, text="Decompress", width=120, fg_color="#1e1e1e",
                hover_color="#333333", command=lambda: menuHandler(Decompress)).pack(side="left", padx=5, pady=5)

    ctk.CTkButton(MENU, text="Transfer Data", width=120, fg_color="#1e1e1e",
                hover_color="#333333", command=lambda: menuHandler(TransferData)).pack(side="left", padx=5, pady=5)

    ctk.CTkButton(MENU, text="Log Manager", width=120, fg_color="#1e1e1e",
                hover_color="#333333", command=lambda: menuHandler(LogManager)).pack(side="left", padx=5, pady=5)

    menuHandler(Compress)

# Main Func
def main():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    SCREEN_ROOT.geometry("900x500")
    SCREEN_ROOT.title("Project Algoritma dan Pemrograman")

    setupMenu()
    SCREEN_ROOT.mainloop()


if __name__ == "__main__":
    main()
