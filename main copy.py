import customtkinter as ctk
from tkinter import ttk, messagebox, filedialog
from PIL import Image

# =======================
# SETTING APLIKASI
# =======================
ctk.set_appearance_mode("dark")          # light / dark / system
ctk.set_default_color_theme("blue")      # blue / dark-blue / green

root = ctk.CTk()
root.title("All CustomTkinter Basic Elements")
root.geometry("900x700")

# FRAME SCROLL (AGAR BANYAK ELEMEN MUAT)
scroll_frame = ctk.CTkScrollableFrame(root, width=850, height=650)
scroll_frame.pack(padx=10, pady=10, fill="both", expand=True)


# ==============================================
# 1. LABEL
# ==============================================
ctk.CTkLabel(scroll_frame, text="⭐ CustomTkinter Basic Elements", 
             font=("Arial", 22, "bold")).pack(pady=10)

ctk.CTkLabel(scroll_frame, text="Label Example").pack(pady=5)


# ==============================================
# 2. ENTRY
# ==============================================
ctk.CTkLabel(scroll_frame, text="Entry").pack()
entry = ctk.CTkEntry(scroll_frame, width=300, placeholder_text="Masukkan teks...")
entry.pack(pady=5)


# ==============================================
# 3. BUTTON
# ==============================================
def on_click():
    messagebox.showinfo("Info", f"Isi Entry: {entry.get()}")

button = ctk.CTkButton(scroll_frame, text="Klik Saya", command=on_click)
button.pack(pady=10)


# ==============================================
# 4. CHECKBOX
# ==============================================
ctk.CTkLabel(scroll_frame, text="CheckBox").pack()
check = ctk.CTkCheckBox(scroll_frame, text="Setuju")
check.pack(pady=5)


# ==============================================
# 5. SWITCH
# ==============================================
ctk.CTkLabel(scroll_frame, text="Switch (Toggle)").pack()
switch = ctk.CTkSwitch(scroll_frame, text="Aktifkan")
switch.pack(pady=5)


# ==============================================
# 6. RADIO BUTTON
# ==============================================
ctk.CTkLabel(scroll_frame, text="Radio Button").pack()
gender = ctk.StringVar(value="L")

ctk.CTkRadioButton(scroll_frame, text="Laki-laki", variable=gender, value="L").pack()
ctk.CTkRadioButton(scroll_frame, text="Perempuan", variable=gender, value="P").pack(pady=5)


# ==============================================
# 7. COMBOBOX
# ==============================================
ctk.CTkLabel(scroll_frame, text="ComboBox").pack()
combo = ctk.CTkComboBox(scroll_frame, values=["Admin", "User", "Guest"])
combo.pack(pady=5)


# ==============================================
# 8. OPTION MENU
# ==============================================
ctk.CTkLabel(scroll_frame, text="OptionMenu").pack()
opt = ctk.CTkOptionMenu(scroll_frame, values=["Red", "Blue", "Green"])
opt.pack(pady=5)


# ==============================================
# 9. SLIDER
# ==============================================
ctk.CTkLabel(scroll_frame, text="Slider").pack()
slider = ctk.CTkSlider(scroll_frame, from_=0, to=100, width=300)
slider.pack(pady=5)


# ==============================================
# 10. PROGRESS BAR
# ==============================================
ctk.CTkLabel(scroll_frame, text="Progress Bar").pack()
progress = ctk.CTkProgressBar(scroll_frame, width=300)
progress.pack(pady=5)
progress.set(0.6)  # 60%


# ==============================================
# 11. TAB VIEW
# ==============================================
ctk.CTkLabel(scroll_frame, text="Tab View").pack()
tabs = ctk.CTkTabview(scroll_frame, width=500, height=200)
tabs.pack(pady=10)

tabs.add("Home")
tabs.add("Setting")

ctk.CTkLabel(tabs.tab("Home"), text="Ini Tab Home").pack(pady=10)
ctk.CTkLabel(tabs.tab("Setting"), text="Ini Tab Setting").pack(pady=10)


# ==============================================
# 12. FRAME (Group)
# ==============================================
ctk.CTkLabel(scroll_frame, text="Frame").pack()
frame_box = ctk.CTkFrame(scroll_frame)
frame_box.pack(pady=10)

ctk.CTkLabel(frame_box, text="Di dalam Frame").pack(padx=20, pady=20)


# ==============================================
# 13. SCROLLABLE FRAME (Sudah digunakan di atas)
# ==============================================
ctk.CTkLabel(scroll_frame, text="ScrollableFrame sudah digunakan di seluruh halaman").pack(pady=5)


# ==============================================
# 14. IMAGE (CTkImage)
# ==============================================
ctk.CTkLabel(scroll_frame, text="Image").pack(pady=10)
try:
    image = ctk.CTkImage(light_image=Image.open("example.png"), size=(150,150))
    ctk.CTkLabel(scroll_frame, image=image, text="").pack()
except:
    ctk.CTkLabel(scroll_frame, text="Tambahkan file example.png agar image tampil.").pack()


# ==============================================
# 15. FILE DIALOG
# ==============================================
def select_file():
    f = filedialog.askopenfilename()
    messagebox.showinfo("File Dipilih", f)

ctk.CTkButton(scroll_frame, text="Open File Dialog", command=select_file).pack(pady=10)


# ==============================================
# 16. TABLE (Treeview)
# ==============================================
ctk.CTkLabel(scroll_frame, text="Table (Treeview)").pack(pady=10)

table = ttk.Treeview(scroll_frame, columns=("ID", "Nama", "Email"), show="headings", height=5)
table.heading("ID", text="ID")
table.heading("Nama", text="Nama")
table.heading("Email", text="Email")

table.insert("", "end", values=(1, "John Doe", "john@mail.com"))
table.insert("", "end", values=(2, "Jane", "jane@mail.com"))

table.pack(pady=10)


# ==============================================
# RUN APP
# ==============================================
root.mainloop()
