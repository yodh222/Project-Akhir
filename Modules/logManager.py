import customtkinter as ctk

class LogManager(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.pack(fill="both", expand=True)

        ctk.CTkLabel(self, text="Halaman Log Manager", font=("Arial", 22)).pack(pady=20)
        ctk.CTkButton(self, text="Lihat Log").pack(pady=10)
