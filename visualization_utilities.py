from tensorflow.keras.utils import plot_model
from PIL import Image
import os
import tkinter as tk
from tkinter import messagebox, filedialog

def visualize_model(model, output_dir=None):
    if not model:
        messagebox.showwarning("Warning", "Model not loaded. Please train or load a model first.")
        return
    
    try:
        # Prompt the user to select an output directory
        if not output_dir:
            root = tk.Tk()
            root.withdraw()  # Hide the main window
            output_dir = filedialog.askdirectory(title="Select Output Directory")
        
        if not output_dir:
            messagebox.showinfo("Info", "Model architecture visualization canceled.")
            return
        
        # Construct the full path for saving the model architecture image
        output_path = os.path.join(output_dir, "model_architecture.png")
        
        # Save the model's architecture to an image file (specify format as needed)
        plot_model(model, to_file=output_path, show_shapes=True, show_layer_names=True, dpi=96)  # Use dpi to control image resolution
        
        # Display the model architecture
        img = Image.open(output_path)
        img.show()
        
        # Cleanup: Delete the generated image
        if os.path.exists(output_path):
            os.remove(output_path)
        
        # Optionally: Provide user feedback
        messagebox.showinfo("Info", "Model architecture visualization completed.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
