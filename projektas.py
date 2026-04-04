from PIL import Image, ImageGrab
import pytesseract
import keyboard
import tkinter as tk
import pyperclip
import ctypes
import datetime
import os
import json
import cutie #tam menu pasirinkimui
import shutil
from plyer import notification #notifications


ctypes.windll.shcore.SetProcessDpiAwareness(2) #kadangi windows scale 150%

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

starttime = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
session_log = f"session_log_{starttime}.txt"


if os.path.exists("settings.json"):
    with open("settings.json", "r") as f:
        settings = json.load(f)

else:
    print("-- First time settings --")

    languages = ["eng", "lit"]
    print("Choose a language:")
    chosen_language = languages[cutie.select(languages)]

    if cutie.prompt_yes_or_no("Do you want to save the screenshots of this session?"):
        sc_choice = True
    else:
        sc_choice = False

    settings = {
        "language": chosen_language,
        "sc_choice": sc_choice
    }

    with open("settings.json", "w") as f:
        json.dump(settings, f)


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

        canvas.bind('<BackSpace>', close)

        root.mainloop()
        return(region)

    region = region_select()
    if region == None:
        print("Screenshot canceled")
        return
    
    width = region[2] - region[0]
    height = region[3] - region[1]

    if width < 5 or height < 5:
        print("Too small area")
        return

    image = ImageGrab.grab(bbox =(region))

    d = datetime.datetime.now()
    date = d.strftime('%Y-%m-%d_%H-%M-%S')
    day = d.strftime('%Y-%m-%d')
    
    if (settings["sc_choice"] == True):
        if not os.path.exists("Screenshots"):
            os.mkdir("Screenshots")
        image.save(f"Screenshots/screenshot{date}.png")

    image.save("screenshot.png")
    print("Screenshot saved!")

    #windows notification
    notification.notify(
        title="Screenshot script",
        message="Screenshot taken!",
        timeout=5
    )

    img = Image.open('screenshot.png')

    # pats teksto nuskaitymas
    gray_image = img.convert("L")
    text = pytesseract.image_to_string(gray_image, lang=settings["language"])
    clean_text = text.replace("\x0c", "").strip()

    history_log = f"hisotry_log_{day}.txt"

    if clean_text != "":
        print(clean_text)

        #isvedimas i txt laikina log tik sios sesijos
        with open(session_log, "a", encoding='utf-8') as f:
            f.write(f"{date}\n")
            f.write("")
            f.write(f"{clean_text}\n")
            f.write("")
            f.write("----------------------\n")
            f.write("")

        #isvedimas i txt history log 
        with open(history_log, "a", encoding='utf-8') as fh:
            fh.write(f"{date}\n")
            fh.write("")
            fh.write(f"{clean_text}\n")
            fh.write("")
            fh.write("----------------------\n")
            fh.write("")

        #clipboard
        pyperclip.copy(clean_text)
        pyperclip.paste()

    #screenshot trinimas 
    os.remove('screenshot.png')
   
def log_clean_up():
    today = datetime.datetime.now().strftime('%Y-%m-%d')

    for file in os.listdir():
        if file.endswith(".txt"):
            if today not in file:
                os.remove(file)

log_clean_up()

keyboard.add_hotkey("ctrl+shift+a", take_screenshot)
print("Press Ctrl+Shift+A to screenshot, Esc to quit")
keyboard.wait('esc')

#session log istrynimas
if os.path.exists(session_log):
    os.remove(session_log)
    
#sesijos screenshotu directorijos trynimas
if os.path.exists("Screenshots"):
    shutil.rmtree("Screenshots")