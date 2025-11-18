import pyautogui
import time

# Wait 3 seconds so you can switch to another window
print("Move your mouse pointer within 3 seconds...")
time.sleep(3)

# # Move cursor to absolute position (x=500, y=300) in 1 second
# pyautogui.moveTo(500, 300, duration=1)

# Move cursor relative to current position
pyautogui.moveRel(100, 0, duration=0.5)  # move right by 100 pixels

# # Click once
# pyautogui.click()

print("Cursor moved successfully!")
