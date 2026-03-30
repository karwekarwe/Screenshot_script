from PIL import Image, ImageGrab
import pytesseract
import keyboard
import tkinter as tk
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
        region = (x, y, event.x, event.y)
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


gray_image = img.convert("L")
text = pytesseract.image_to_string(gray_image)
clean_text = text.replace("\x0c", "").strip()
print(clean_text)
