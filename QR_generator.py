import segno
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

def static_generator():
    data = input("Wprowadz zmienna do zapisu:\n")
    size = input("Podaj rozmiar:\n") or 10
    border = input("Wielkosc ramki:\n") or 2
    dark = input("Kolor qr:\n") or "#000000"#ewentualnie None, nazwa/hex/rgb
    light = input("Kolor tla:\n") or None #ewentualnie None, nazwa/hex/rgb
    rotate = input("obrot:\n") or 0

    static_save_path = os.path.join(current_dir, "QR_CODE.png")
    save_path = input(f"Podaj ścieżkę zapisu pliku (z nazwą pliku i rozszerzeniem) [domyślnie {static_save_path}]:\n") or static_save_path


    qrcode = segno.make(data, micro=False)
    rotated_qrcode = qrcode.to_pil(
                scale=int(size),
                border=int(border),
                dark=dark,
                light=light
    ).rotate(int(rotate), expand=True)

    rotated_qrcode.save(save_path) #png akceptuje tylko całkowite wartości, do zmiennoprzecinkowych musimy tworzyć svg

def dynamic_generator():
    data = input("Wprowadz zmienna do zapisu:\n")
    size = input("Podaj rozmiar:\n") or 10
    border = input("Wielkosc ramki:\n") or 2
    dark = input("Kolor qr:\n") or "#000000"  # ewentualnie None, nazwa/hex/rgb
    light = input("Kolor tla:\n") or None  # ewentualnie None, nazwa/hex/rgb
    background = input("sciezka do gifu albo zdjecia")

    dynamic_save_path = os.path.join(current_dir, "QR_CODE.gif")
    save_path = input(f"Podaj ścieżkę zapisu pliku (z nazwą pliku i rozszerzeniem) [domyślnie {dynamic_save_path}]:\n") or dynamic_save_path

    qrcode = segno.make(data, error='h')
    qrcode.to_artistic(
        background=background,
        target=save_path,
        scale=int(size),
        border=int(border),
        dark=dark,
        light=light
    )