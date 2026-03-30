#istrint ta screenshota po visko
# isvest i txt faila
# idet i clipboard teksta
# settings: kalba - ar visas ekranas ar pasirinkta dalis; kalba; ar istrint screenshota; ar istrint output file; ar as it is ar istrint taprus and stuff

from PIL import Image, ImageGrab
import pytesseract
import keyboard
import tkinter as tk
import pyperclip
import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(2) #kadangi windows scale 150%

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def region_select():
    root = tk.Tk()
    root.attributes('-fullscreen', True)
    root.attributes('-alpha', 0.3)
    root.attributes('-topmost', True)

    canvas = tk.Canvas(root)

    x = 0
    y = 0

    def on_click(event):
        nonlocal x, y 
        x, y = event.x, event.y


    canvas.bind("<Button-1>", on_click)
    canvas.pack(fill='both', expand=True)

    rect = None

    def on_drag(event):
        nonlocal rect
        if rect:
            canvas.delete(rect)   
        rect = canvas.create_rectangle(
        x, y, event.x, event.y,
        outline='red', width=2, fill='white')


    canvas.bind("<B1-Motion>", on_drag)

    region = None

    def on_release(event):
        nonlocal region
        x1, y1 = x, y
        x2, y2 = event.x, event.y

        region = (min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2))
        root.destroy() 

    canvas.bind('<ButtonRelease-1>', on_release)

    root.mainloop()
    return(region)


def take_screenshot():
    region = region_select()
    image = ImageGrab.grab(bbox =(region))
    image.save("screenshot.png")
    print("Screenshot saved!")

keyboard.add_hotkey("ctrl+shift+a", take_screenshot)
print("Running... Press Ctrl+Shift+A to screenshot, Esc to quit")
keyboard.wait('esc')

img = Image.open('screenshot.png')

# pats teksto nuskaitymas
gray_image = img.convert("L")
text = pytesseract.image_to_string(gray_image)
clean_text = text.replace("\x0c", "").strip()
print(clean_text)


#isvedimas i txt
with open("ouptut.txt", "w") as f:
  f.write(clean_text)

#clipboard
pyperclip.copy(clean_text)
pyperclip.paste()