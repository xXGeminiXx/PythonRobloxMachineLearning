import os
import time
import pyautogui
from PIL import ImageGrab, Image
import logging
from tkinter import simpledialog, messagebox

def capture_and_label(selected_area, model, CLASSES, predict_block_type, IMAGE_SAVE_PATH):
    if not selected_area:
        messagebox.showerror("Error", "Please select an area first.")
        return
    
    try:
        buffer = 50
        x, y = pyautogui.position()
        captured_image = ImageGrab.grab(bbox=(x - buffer, y - buffer, x + buffer, y + buffer))
        
        predicted_label = "unknown"
        
        if not model:
            messagebox.showwarning("Warning", "Model not loaded. Please train or load a model first.")
            return
        
        predicted_label = predict_block_type(captured_image)
        
        captured_image.show()
        
        label = simpledialog.askstring("Label the Block", "What block is this?", initialvalue=predicted_label)
        
        if label and label not in CLASSES:
            messagebox.showwarning("Warning", f"Unknown label '{label}'. Please use one of the predefined labels: {', '.join(CLASSES)}.")
            return
        
        # Confirm with the user before saving the image
        confirmation = messagebox.askyesno("Confirm", "Do you want to save this image?")
        
        if confirmation:
            # Sanitize the label for file naming
            sanitized_label = label.replace(" ", "_").replace("/", "_")
            
            # Save the captured image with a timestamped filename
            image_filename = f"{sanitized_label}_{time.strftime('%Y%m%d%H%M%S')}.png"
            image_path = os.path.join(IMAGE_SAVE_PATH, image_filename)
            captured_image.save(image_path)
            
            # Provide user feedback
            messagebox.showinfo("Info", f"Image saved as: {image_path}")
    except Exception as e:
        error_message = f"An error occurred while capturing and labeling: {str(e)}"
        logging.error(error_message)
        messagebox.showerror("Error", error_message)

    if not model:
        messagebox.showwarning("Warning", "Model not loaded. Please train or load a model first.")
        return
    
    # Ask the user for the number of images to capture
    num_images = simpledialog.askinteger("Batch Capture", "How many images do you want to capture?", initialvalue=10)
    
    if num_images is None:
        return  # User canceled
    
    for _ in range(num_images):
        try:
            buffer = 50
            x, y = pyautogui.position()
            captured_image = ImageGrab.grab(bbox=(x - buffer, y - buffer, x + buffer, y + buffer))
            
            predicted_label = "unknown"
            
            try:
                predicted_label = predict_block_type(captured_image)
            except Exception as e:
                logging.error(f"Error predicting block type: {str(e)}")
            
            captured_image.show()
            
            label = simpledialog.askstring("Label the Block", "What block is this?", initialvalue=predicted_label)
            
            if label and label not in CLASSES:
                messagebox.showwarning("Warning", f"Unknown label '{label}'. Please use one of the predefined labels: {', '.join(CLASSES)}.")
                return
            
            # Confirm with the user before saving each image
            confirmation = messagebox.askyesno("Confirm", "Do you want to save this image?")
            
            if confirmation:
                # Sanitize the label for file naming
                sanitized_label = label.replace(" ", "_").replace("/", "_")
                
                # Save the captured image with a timestamped filename
                image_filename = f"{sanitized_label}_{time.strftime('%Y%m%d%H%M%S')}.png"
                image_path = os.path.join(IMAGE_SAVE_PATH, image_filename)
                captured_image.save(image_path)
                
                # Provide user feedback
                messagebox.showinfo("Info", f"Image saved as: {image_path}")
        except Exception as e:
            error_message = f"An error occurred while capturing and labeling: {str(e)}"
            logging.error(error_message)
            messagebox.showerror("Error", error_message)
