from PIL import Image, ImageGrab
import pytesseract
import keyboard
import tkinter as tk
import pyperclip
import ctypes
import datetime
import os
import cutie #tam menu pasirinkimui

ctypes.windll.shcore.SetProcessDpiAwareness(2) #kadangi windows scale 150%

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def take_screenshot():

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

# paspaudus esc turetu issijungti overlay bet neveikia
        def close(event):
            nonlocal region
            region = None
            root.destroy()

        canvas.bind('<Escape>', close)


        root.mainloop()
        return(region)



    region = region_select()
    if region == None:
        print("Screenshot canceled")
        return
    
    width = region[2] - region[0]
    height = region[3] - region[1]

    if width < 5 or height < 5:
        print("Per mažas dydis")
        return

    image = ImageGrab.grab(bbox =(region))
    image.save("screenshot.png")
    print("Screenshot saved!")

    img = Image.open('screenshot.png')

    # pats teksto nuskaitymas
    gray_image = img.convert("L")
    text = pytesseract.image_to_string(gray_image)
    clean_text = text.replace("\x0c", "").strip()

    d = datetime.datetime.now()
    date = d.strftime('%Y-%m-%d_%H-%M-%S')

    if clean_text != "":
        print(clean_text)

        #isvedimas i txt laikina log tik sios sesijos
        with open(f"ouptut_{date}.txt", "a") as f:
            f.write(f"{date}\n")
            f.write("")
            f.write(f"{clean_text}\n")
            f.write("")
            f.write("----------------------\n")
            f.write("")

        #isvedimas i txt history log 
        with open("history.txt", "a") as fh:
            fh.write(f"{date}\n")
            fh.write("")
            fh.write(f"{clean_text}\n")
            fh.write("")
            fh.write("----------------------\n")
            fh.write("")


        #clipboard
        pyperclip.copy(clean_text)
        pyperclip.paste()

    #pause 
  #  os.system("pause")

    #failu trinimas - pasirinkimas ar nori issaugot screenshotus
    os.remove('screenshot.png')

    if clean_text != "":
        os.remove(f"ouptut_{date}.txt")




keyboard.add_hotkey("ctrl+shift+a", take_screenshot)
print("Running... Press Ctrl+Shift+A to screenshot, Esc to quit")
keyboard.wait('esc')

