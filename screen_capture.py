import logging
import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.model_selection import train_test_split
from PIL import ImageGrab
import pyautogui
import time
import tkinter as tk
from tkinter import simpledialog, messagebox
import threading

# Configure logging
logging.basicConfig(filename='application.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Function to capture an area of the screen
def capture_area(x, y, buffer=50):
    try:
        captured_image = ImageGrab.grab(bbox=(x - buffer, y - buffer, x + buffer, y + buffer))
        return captured_image
    except Exception as e:
        logging.error(f"Error during image capture: {str(e)}")
        return None

# Function to predict block type from an image
def predict_block_type(image, model):
    # Preprocess the image (you may need to adapt this part based on your model's requirements)
    image = image.resize((224, 224))  # Resize the image to your model's input size
    image = np.array(image)  # Convert PIL image to NumPy array
    image = image / 255.0  # Normalize the image data (assuming your model requires this)
    
    # Perform inference
    predictions = model.predict(np.expand_dims(image, axis=0))
    
    # Decode predictions and get the predicted label
    predicted_class = np.argmax(predictions)
    return predicted_class

# Function to capture an area and predict its block type
def capture_and_predict_block_type(model, label_var):
    try:
        x, y = pyautogui.position()
        captured_image = capture_area(x, y)
        
        if captured_image:
            predicted_label = predict_block_type(captured_image, model)
            label_var.set(f"Predicted Block: {predicted_label}")
            captured_image.show()
    except Exception as e:
        logging.error(f"Error during image capture and prediction: {str(e)}")
        label_var.set("Status: Capture and prediction failed!")

# Function to start real-time prediction
def start_real_time_prediction(model, label_var):
    global running_real_time_prediction
    if not model:
        messagebox.showwarning("Warning", "Model not loaded. Please train or load a model first.")
        return
    running_real_time_prediction = True
    threading.Thread(target=real_time_prediction, args=(model, label_var)).start()

# Function to stop real-time prediction
def stop_real_time_prediction():
    global running_real_time_prediction
    running_real_time_prediction = False

# Function to perform real-time prediction
def real_time_prediction(model, label_var):
    global running_real_time_prediction
    while running_real_time_prediction:
        x, y = pyautogui.position()
        captured_image = capture_area(x, y)
        
        if captured_image:
            predicted_label = predict_block_type(captured_image, model)
            label_var.set(f"Predicted Block: {predicted_label}")
        time.sleep(0.5)  # Adding a short delay for performance

# Function to select a screen area
def select_screen_area():
    global overlay, start_x, start_y
    overlay = tk.Tk()
    overlay.attributes('-alpha', 0.3)
    overlay.geometry(f"{overlay.winfo_screenwidth()}x{overlay.winfo_screenheight()}+0+0")
    overlay.bind("<Button-1>", on_press)
    overlay.bind("<ButtonRelease-1>", on_release)
    overlay.mainloop()

# Callback for capturing the starting position of the selection area
def on_press(event):
    global start_x, start_y
    start_x, start_y = event.x_root, event.y_root

# Callback for capturing the ending position of the selection area
def on_release(event):
    global selected_area
    end_x, end_y = event.x_root, event.y_root
    selected_area = (start_x, start_y, end_x, end_y)
    overlay.destroy()

# Function to clear captured data
def clear_captured_data():
    global model
    confirm = messagebox.askyesno("Confirm", "Do you really want to clear all captured data?")
    if confirm:
        for class_name in CLASSES:
            folder_path = os.path.join(IMAGE_SAVE_PATH, class_name)
            for image_file in os.listdir(folder_path):
                os.remove(os.path.join(folder_path, image_file))
        model = None
        status_var.set("Data cleared. Model reset.")

    for file in os.listdir(IMAGE_SAVE_PATH):
        file_path = os.path.join(IMAGE_SAVE_PATH, file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            logging.error(f"Failed to delete file {file_path}. Error: {e}")
    messagebox.showinfo("Info", "Captured data cleared!")

# Your existing code
if __name__ == "__main__":
    # Load your model and set up any required preprocessing
    model = None  # Load your trained model here

    # Define your classes (modify this list to match your actual classes)
    CLASSES = ['class_0', 'class_1', 'class_2']

    # Set the path where captured images will be saved
    IMAGE_SAVE_PATH = 'captured_images'

    # Create folders for each class if they don't exist
    os.makedirs(IMAGE_SAVE_PATH, exist_ok=True)
    for class_name in CLASSES:
        os.makedirs(os.path.join(IMAGE_SAVE_PATH, class_name), exist_ok=True)

    # Create a GUI window for user interactions
    root = tk.Tk()
    root.title("Block Type Prediction")
    root.geometry("400x400")

    # Create a label for displaying the prediction result
    label_var = tk.StringVar()
    label_var.set("Predicted Block: None")
    prediction_label = tk.Label(root, textvariable=label_var)
    prediction_label.pack(pady=20)

    # Create buttons for actions
    capture_and_predict_button = tk.Button(root, text="Capture and Predict", command=lambda: capture_and_predict_block_type(model, label_var))
    start_real_time_button = tk.Button(root, text="Start Real-Time Prediction", command=lambda: start_real_time_prediction(model, label_var))
    stop_real_time_button = tk.Button(root, text="Stop Real-Time Prediction", command=stop_real_time_prediction)
    clear_data_button = tk.Button(root, text="Clear Captured Data", command=clear_captured_data)
    select_area_button = tk.Button(root, text="Select Screen Area", command=select_screen_area)
    exit_button = tk.Button(root, text="Exit", command=root.quit)

    capture_and_predict_button.pack()
    start_real_time_button.pack()
    stop_real_time_button.pack()
    clear_data_button.pack()
    select_area_button.pack()
    exit_button.pack()

    # Create a status label
    status_var = tk.StringVar()
    status_var.set("Status: Ready")
    status_label = tk.Label(root, textvariable=status_var)
    status_label.pack(pady=10)

    # Start the GUI
    root.mainloop()
def batch_capture_and_label(num_images=10):
    global selected_area
    if not selected_area:
        messagebox.showerror("Error", "Please select an area first.")
        return
    
    if not model:
        messagebox.showwarning("Warning", "Model not loaded. Please train or load a model first.")
        return
    
def reset_screen_selection():
    global selected_area
    selected_area = None
    status_var.set("Status: Screen area reset. Please select again.")
    select_screen_area()

# Adding the "Reset Screen Area" button to the GUI

if __name__ == "__main__":
    root = tk.Tk()
    reset_area_button = tk.Button(root, text="Reset Screen Area", command=reset_screen_selection)
    

    reset_area_button.pack(pady=10)
    root.mainloop()
    

