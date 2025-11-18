import tkinter as tk
import pyautogui
import pygetwindow as gw
import time

# === Remember the last active window before keyboard opens ===
try:
    last_window = gw.getActiveWindow()
except:
    last_window = None

root = tk.Tk()
root.title("Virtual Keyboard")
root.attributes("-topmost", True)
root.geometry("800x300")

def press_key(key):
    global last_window

    # Refocus last active window (so typing goes there)
    if last_window:
        try:
            last_window.activate()
        except:
            pass

    time.sleep(0.05)  # small delay for focus switch

    # Send actual key
    if key == "SPACE":
        pyautogui.press("space")
    elif key == "ENTER":
        pyautogui.press("enter")
    elif key == "BACKSPACE":
        pyautogui.press("backspace")
    elif key == "TAB":
        pyautogui.press("tab")
    else:
        pyautogui.write(key)

    # Return focus to keyboard
    root.attributes("-topmost", True)
    root.focus_force()

# === Layout ===
keys = [
    ['1','2','3','4','5','6','7','8','9','0','BACKSPACE'],
    ['Q','W','E','R','T','Y','U','I','O','P'],
    ['A','S','D','F','G','H','J','K','L','ENTER'],
    ['Z','X','C','V','B','N','M',',','.','?'],
    ['SPACE']
]

for row_index, row in enumerate(keys):
    for col_index, key in enumerate(row):
        if key == "SPACE":
            btn = tk.Button(root, text="SPACE", width=60, height=2,
                            command=lambda k=key: press_key(k))
            btn.grid(row=row_index, column=col_index, columnspan=10, pady=5)
        else:
            btn = tk.Button(root, text=key, width=6, height=2,
                            command=lambda k=key: press_key(k))
            btn.grid(row=row_index, column=col_index, padx=2, pady=5)

root.mainloop()


