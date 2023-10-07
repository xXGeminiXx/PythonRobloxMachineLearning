import os
import logging
import tkinter as tk
from tkinter import messagebox, simpledialog  # Added 'simpledialog'
from PIL import ImageGrab, Image
import pyautogui  # Added 'pyautogui'

# Set your image save path here
IMAGE_SAVE_PATH = './captured_data'

def clear_captured_data(CLASSES, IMAGE_SAVE_PATH):
    # Confirm with the user before clearing data
    confirmation = messagebox.askyesno("Confirm", "Are you sure you want to clear captured data?")
    
    if not confirmation:
        return
    
    try:
        # Clear data in class subdirectories
        for class_name in CLASSES:
            folder_path = os.path.join(IMAGE_SAVE_PATH, class_name)
            for image_file in os.listdir(folder_path):
                image_path = os.path.join(folder_path, image_file)
                os.remove(image_path)

        # Clear any remaining files in the main directory
        for file in os.listdir(IMAGE_SAVE_PATH):
            file_path = os.path.join(IMAGE_SAVE_PATH, file)
            if os.path.isfile(file_path):
                os.unlink(file_path)
        
        # Provide user feedback
        messagebox.showinfo("Info", "Captured data cleared successfully!")
    except Exception as e:
        error_message = f"An error occurred while clearing data: {str(e)}"
        logging.error(error_message)
        messagebox.showerror("Error", error_message)

if __name__ == "__main__":
    # Example usage:
    CLASSES = ["class1", "class2"]
    clear_captured_data(CLASSES, IMAGE_SAVE_PATH)


def capture_click_area(selected_area=None):
    if not selected_area:
        messagebox.showerror("Error", "Please select an area first.")
        return
    
    try:
        buffer = 50
        x, y = pyautogui.position()
        captured_image = ImageGrab.grab(bbox=(x - buffer, y - buffer, x + buffer, y + buffer))
        
        # Display the captured image
        captured_image.show()
    except Exception as e:
        logging.error(f"Error capturing the click area: {e}")
        messagebox.showerror("Error", "Error capturing the click area.")


def _batch_capture_and_label(selected_area=None, IMAGE_SAVE_PATH=IMAGE_SAVE_PATH):
    if not selected_area:
        messagebox.showerror("Error", "Please select an area first.")
        return

    try:
        buffer = 50
        label_count = {}
        
        while True:
            x, y = pyautogui.position()
            captured_image = ImageGrab.grab(bbox=(x - buffer, y - buffer, x + buffer, y + buffer))
            
            # Display the captured image and ask for label
            captured_image.show()
            label = simpledialog.askstring("Label the Block", "What block is this?")
            
            if not label:  # If user presses Cancel or enters nothing, stop the loop
                break
            
            # Save the image with the provided label
            label_folder = os.path.join(IMAGE_SAVE_PATH, label)
            os.makedirs(label_folder, exist_ok=True)
            
            # Count images of the same label to generate unique file names
            label_count[label] = label_count.get(label, 0) + 1
            image_path = os.path.join(label_folder, f"{label}_{label_count[label]}.png")
            captured_image.save(image_path)
            
    except Exception as e:
        logging.error(f"Error during batch capture and label: {e}")
        messagebox.showerror("Error", "Error during batch capture and label.")


def batch_capture_and_label(selected_area=None, IMAGE_SAVE_PATH=IMAGE_SAVE_PATH):
    if not selected_area:
        messagebox.showerror("Error", "Please select an area first.")
        return

    buffer = 50
    label_count = {}

    while True:
        # Capture the screen area around the mouse pointer
        x, y = pyautogui.position()
        captured_image = ImageGrab.grab(bbox=(x - buffer, y - buffer, x + buffer, y + buffer))
        
        # Display the captured image and ask for a label
        captured_image.show()
        label = simpledialog.askstring("Label the Image", "What is this image?")
        
        # If the user provides no label or presses cancel, break out of the loop
        if not label:
            break
        
        # Save the image to the respective label folder
        label_folder = os.path.join(IMAGE_SAVE_PATH, label)
        os.makedirs(label_folder, exist_ok=True)
        
        label_count[label] = label_count.get(label, 0) + 1
        image_path = os.path.join(label_folder, f"{label}_{label_count[label]}.png")
        captured_image.save(image_path)
