import customtkinter as ctk
from tkinter import filedialog
import segno
from PIL import Image, ImageTk, ImageOps


def generate_qr_code(data, scale=10, qr_color="black", background=None, rotation=0):
    qr = segno.make(data)
    qr_img = qr.to_pil(scale=scale, dark=qr_color)

    if rotation != 0:
        qr_img = qr_img.rotate(rotation, expand=True)

    return qr_img


def update_qr_preview():
    scale = size_slider.get()
    qr_color = qr_color_entry.get()
    if style_switch.get() == "Statyczny":
        rotation = int(rotation_entry.get())
        qr_img = generate_qr_code("Sample QR Code", scale=scale, qr_color=qr_color, rotation=rotation)
    else:
        bg_file = bg_file_entry.get()
        qr_img = generate_qr_code("Sample QR Code", scale=scale, qr_color=qr_color, background=bg_file)

    qr_img.thumbnail((400, 400))  # Ensure the preview is a reasonable size

    qr_img_tk = ImageTk.PhotoImage(qr_img)
    qr_preview_label.configure(image=qr_img_tk)
    qr_preview_label.image = qr_img_tk


def choose_file():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.gif")])
    bg_file_entry.delete(0, ctk.END)
    bg_file_entry.insert(0, file_path)


def toggle_options():
    if style_switch_var.get() == 1:
        dynamic_frame.grid_remove()
        static_frame.grid()
    elif style_switch_var.get() == 2:
        static_frame.grid_remove()
        dynamic_frame.grid()


app = ctk.CTk()
app.geometry("1000x800")
app.title("QR Codes Generator")

# Podział ekranu na dwie części

right_frame = ctk.CTkFrame(app)
right_frame.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)
right_frame.grid_rowconfigure(1, weight=1)

left_frame = ctk.CTkFrame(app)
left_frame.grid(row=0, column=0, sticky="nswe", padx=20, pady=20)
left_frame.grid_rowconfigure(0, weight=1)
#left_frame.grid_rowconfigure(1, weight=3)

upper_frame = ctk.CTkFrame(left_frame)
upper_frame.grid(row=0, column=0, sticky="n")
#upper_frame.grid_rowconfigure(0, weight=1)

bottom_frame = ctk.CTkFrame(left_frame)
bottom_frame.grid(row=1, column=0, sticky="s")
#bottom_frame.grid_rowconfigure(1, weight=3)


app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=1)
app.grid_rowconfigure(0, weight=1)
app.grid_rowconfigure(1, weight=1)


# Przełącznik stylu tła
style_switch_var = ctk.IntVar(value=1)  # Tworzy zmienną int, domyślnie ustawioną na 1
style_switch_static = ctk.CTkRadioButton(upper_frame, text="Statyczny", variable=style_switch_var, value=1, command=toggle_options)
style_switch_dynamic = ctk.CTkRadioButton(upper_frame, text="Dynamiczny", variable=style_switch_var, value=2, command=toggle_options)

style_switch_static.grid(row=1, column=0, pady=10, padx=10, sticky="ew")
style_switch_dynamic.grid(row=1, column=1, pady=10, padx=10, sticky="ew")

# Statyczny styl tła
static_frame = ctk.CTkFrame(bottom_frame)
static_frame.grid(row=1, column=0, sticky="nswe")

size_label = ctk.CTkLabel(static_frame, text="Wybierz wielkość QR-kodu:")
size_label.grid(row=0, column=0, pady=10, padx=10, sticky="w")

size_value_label = ctk.CTkLabel(static_frame, text="10")
size_value_label.grid(row=1, column=1, pady=10, padx=10, sticky="e")


def size_slider_callback(value):
    size_value_label.configure(text=str(int(value)))


size_slider = ctk.CTkSlider(static_frame, from_=1, to=20, orientation="horizontal", command=size_slider_callback)
size_slider.set(10)
size_slider.grid(row=1, column=0, pady=10, padx=10, sticky="ew")

qr_color_label = ctk.CTkLabel(static_frame, text="Kolor QR (w formacie #RRGGBB):")
qr_color_label.grid(row=2, column=0, pady=10, padx=10, sticky="w")

qr_color_entry = ctk.CTkEntry(static_frame)
qr_color_entry.grid(row=3, column=0, pady=10, padx=10, sticky="ew")

rotation_label = ctk.CTkLabel(static_frame, text="Kąt obrócenia kodu QR:")
rotation_label.grid(row=4, column=0, pady=10, padx=10, sticky="w")

rotation_entry = ctk.CTkEntry(static_frame)
rotation_entry.grid(row=5, column=0, pady=10, padx=10, sticky="ew")

# Dynamiczny styl tła
dynamic_frame = ctk.CTkFrame(bottom_frame)
dynamic_frame.grid(row=1, column=0, sticky="nswe")
dynamic_frame.grid_remove()

bg_file_button = ctk.CTkButton(dynamic_frame, text="Wybierz plik tła (GIF/PNG)", command=choose_file)
bg_file_button.grid(row=0, column=0, pady=10, padx=10, sticky="ew")

bg_file_entry = ctk.CTkEntry(dynamic_frame)
bg_file_entry.grid(row=1, column=0, pady=10, padx=10, sticky="ew")

qr_color_label_dynamic = ctk.CTkLabel(dynamic_frame, text="Kolor QR (w formacie #RRGGBB):")
qr_color_label_dynamic.grid(row=2, column=0, pady=10, padx=10, sticky="w")

qr_color_entry_dynamic = ctk.CTkEntry(dynamic_frame)
qr_color_entry_dynamic.grid(row=3, column=0, pady=10, padx=10, sticky="ew")

generate_button = ctk.CTkButton(bottom_frame, text="Wygeneruj Kod QR", command=update_qr_preview)
generate_button.grid(row=10, column=0, pady=20, padx=10, sticky="ew")

# Podgląd kodu QR w prawej części ekranu
qr_preview_label = ctk.CTkLabel(right_frame, text="")
qr_preview_label.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

app.mainloop()