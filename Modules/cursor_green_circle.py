import tkinter as tk
import pyautogui

# Settings
RADIUS = 30
COLOR = "lime"   # can use 'red', 'blue', '#00FF00' etc
BORDER = 3
UPDATE_INTERVAL = 10  # in ms

root = tk.Tk()
root.attributes("-topmost", True)
root.attributes("-transparentcolor", "black")
root.overrideredirect(True)  # no border or title bar

# Fullscreen overlay canvas
screen_width, screen_height = pyautogui.size()
canvas = tk.Canvas(root, width=screen_width, height=screen_height, bg='black', highlightthickness=0)
canvas.pack()

circle = canvas.create_oval(0, 0, 0, 0, outline=COLOR, width=BORDER)

def update_circle():
    x, y = pyautogui.position()
    canvas.coords(circle, x - RADIUS, y - RADIUS, x + RADIUS, y + RADIUS)
    root.after(UPDATE_INTERVAL, update_circle)

update_circle()
root.mainloop()
