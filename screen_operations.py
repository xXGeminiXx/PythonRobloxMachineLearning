import logging
import pyautogui
from tkinter import messagebox
from PIL import ImageGrab

# Setting up logging
logging.basicConfig(level=logging.INFO)

# Global variable to store the selected screen area
selected_area = None

def capture_screen_region():
    import tkinter as tk

    # Variables to store starting and ending mouse position
    ix, iy, fx, fy = None, None, None, None

    def on_click(x, y, button, pressed):
        nonlocal ix, iy, fx, fy
        if pressed:
            ix, iy = x, y
        else:
            fx, fy = x, y
            root.quit()

    root = tk.Tk()

    # Get screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Set the full screen size for the transparent tkinter window
    root_geometry = str(screen_width) + 'x' + str(screen_height)
    root.geometry(root_geometry)

    # Make the window transparent and borderless
    root.overrideredirect(True)
    root.wait_visibility(root)
    root.wm_attributes("-alpha", 0.3)

    canvas = tk.Canvas(root, width=screen_width, height=screen_height)
    canvas.config(cursor="cross")
    canvas.pack()

    # Start the mouse listener and tkinter window
    root.mainloop()

    # Capture the selected screen region and return the coordinates
    return ix, iy, fx, fy

def select_screen_area():
    global selected_area
    logging.info("Select screen area function called.")
    ix, iy, fx, fy = capture_screen_region()
    selected_area = (ix, iy, fx, fy)
    logging.info(f"Selected area coordinates: {selected_area}")
    # Optionally capture and save the screenshot for reference
    screenshot_path = 'screenshot_area.png'
    img = ImageGrab.grab(bbox=selected_area)
    img.save(screenshot_path)
    print("Screenshot saved at:", screenshot_path)
    return selected_area

def reset_screen_selection():
    global selected_area
    logging.info("Reset screen selection function called.")
    selected_area = None
    logging.info("Screen selection reset.")
