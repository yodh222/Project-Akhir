import customtkinter as ctk
from tkinter import filedialog

class TransferData(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill="both", expand=True, padx=40, pady=40) 
        
        # GRID SETUP
        self.grid_columnconfigure(0, weight=1)   # Entry full width
        self.grid_columnconfigure(1, weight=0)   # Button fixed width
        self.grid_rowconfigure(10, weight=1)     # Extra bottom space for centering

        # IP Target
        ctk.CTkLabel(
            self, text="IP Target",
            font=("Arial", 15, "bold"),
            anchor="w"
        ).grid(row=0, column=0, sticky="w", pady=(0, 5))

        self.entry_ip = ctk.CTkEntry(self, placeholder_text="Please Enter IP Target (i.e. 192.168.1.1)")
        self.entry_ip.grid(row=1, column=0, sticky="ew", padx=(0,10), pady=5)

        # Port
        ctk.CTkLabel(
            self, text="Port",
            font=("Arial", 15, "bold"),
            anchor="w"
        ).grid(row=4, column=0, sticky="w", pady=(20, 5))

        self.entry_port = ctk.CTkEntry(self, placeholder_text="Please Enter Port (i.e. 22)")
        self.entry_port.grid(row=5, column=0, sticky="ew", padx=(0,10), pady=5)

        # File to be Transfer
        ctk.CTkLabel(
            self, text="File to be Transfer",
            font=("Arial", 15, "bold"),
            anchor="w"
        ).grid(row=6, column=0, sticky="w", pady=(20, 5))

        self.entry_file = ctk.CTkEntry(self, placeholder_text="Select File")
        self.entry_file.grid(row=7, column=0, sticky="ew", padx=(0,10), pady=5)

        ctk.CTkButton(self, text="Browse File", width=140, command=self.search_file).grid(
            row=7, column=1, sticky="w", pady=5
        )

        # Start Compression Button
        ctk.CTkButton(self, text="Send Data", width=160, command=None).grid(
            row=10, column=0, columnspan=2, pady=40
        )

    def search_file(self):
        """Open dialog to select a source file."""
        path = filedialog.askopenfilename()
        if path:
            self.entry_file.delete(0, "end")
            self.entry_file.insert(0, path)
