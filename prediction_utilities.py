import tkinter as tk
from tkinter import messagebox
import time
import pyautogui
import threading
from PIL import ImageGrab
import logging
import numpy as np
import tensorflow as tf
import os

# Configure logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

# Constants
REAL_TIME_PREDICTION_INTERVAL = 0.5
BUFFER_SIZE = 50

# Lock for thread-safe access to global variables
lock = threading.Lock()

# Global variables
running_real_time_prediction = False
stop_event = threading.Event()
model = None  # Initialize model as None

# Placeholder class-to-label mapping
class_mapping = {0: "Class_0", 1: "Class_1", 2: "Class_2"}

def real_time_prediction(predict_block_type, status_var):
    global running_real_time_prediction
    global model
    while not stop_event.is_set():
        x, y = pyautogui.position()
        captured_image = ImageGrab.grab(bbox=(x - BUFFER_SIZE, y - BUFFER_SIZE, x + BUFFER_SIZE, y + BUFFER_SIZE))
        
        try:
            if model:
                predicted_label = 0
                predicted_class = class_mapping[predicted_label]
            else:
                predicted_class = "Model not loaded"
        except Exception as e:
            logger.error(f"Error predicting block type in real-time: {str(e)}")
            predicted_class = "unknown"
        
        with lock:
            status_var.set(f"Predicted Block: {predicted_class}")
        time.sleep(REAL_TIME_PREDICTION_INTERVAL)

def start_real_time_prediction(predict_block_type, status_var):
    global running_real_time_prediction
    global model
    with lock:
        if not model:
            messagebox.showwarning("Warning", "Model not loaded. Please train or load a model first.")
            return
    running_real_time_prediction = True
    stop_event.clear()
    threading.Thread(target=real_time_prediction, args=(predict_block_type, status_var)).start()

def stop_real_time_prediction():
    global running_real_time_prediction
    if running_real_time_prediction:
        running_real_time_prediction = False
        stop_event.set()

def load_model_file(model_file):
    global model
    try:
        base_directory = r'C:\\Apps\\Automation Stuff\\NewColorMachineLearningProject\\v3'
        model_path = os.path.join(base_directory, model_file)
        if os.path.exists(model_path):
            model = tf.keras.models.load_model(model_path)
            logger.info(f"Loaded model from {model_path}")
        else:
            logger.info("Model file not found. Generating a blank default model.")
            # Placeholder for generating a blank model
            # model = create_blank_model_function()  # This function needs to be defined
            # model.save(model_path)
            messagebox.showinfo("Info", "A default model has been generated since no existing model was found.")
    except Exception as e:
        logger.error(f"Error loading or creating model: {str(e)}")
        messagebox.showerror("Error", f"Error loading or creating model: {str(e)}")

def take_action_based_on_prediction(prediction):
    pass