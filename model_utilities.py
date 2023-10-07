import tensorflow as tf
import json

def create_model(num_layers, filter_size, dropout_rate, image_size, num_classes):
    num_layers = num_layers_var.get()
    filter_size = filter_size_var.get()
    dropout_rate = dropout_rate_var.get()
    
    model = Sequential()
    
    # First layer (common for all configurations)
    model.add(Conv2D(32, (filter_size, filter_size), activation='relu', input_shape=(IMAGE_SIZE[0], IMAGE_SIZE[1], 3)))
    model.add(MaxPooling2D((2, 2)))
    
    # Additional layers based on user input
    for _ in range(1, num_layers):
        model.add(Conv2D(32 * (2**_), (filter_size, filter_size), activation='relu'))
        model.add(MaxPooling2D((2, 2)))
    
    model.add(Flatten())
    model.add(Dense(512, activation='relu'))
    model.add(Dropout(dropout_rate))
    model.add(Dense(len(CLASSES), activation='softmax'))
    
    return model

# ... [rest of the code]

import json

def save_model_configuration(num_layers, filter_size, dropout_rate, filename="model_config.json"):
    """
    Save model configuration to a JSON file.

    Args:
        num_layers (int): Number of convolutional layers.
        filter_size (int): Filter size for convolutional layers.
        dropout_rate (float): Dropout rate for regularization.
        filename (str): Name of the JSON file to save the configuration.
    """
    config = {
        "num_layers": num_layers,
        "filter_size": filter_size,
        "dropout_rate": dropout_rate
    }
    
    with open(filename, "w") as f:
        json.dump(config, f, indent=4)  # Indent for better readability

# Example usage:
if __name__ == "__main__":
    num_layers = 3
    filter_size = 3
    dropout_rate = 0.5
    image_size = (128, 128, 3)
    num_classes = 2  # Use '2' for binary classification, or adjust for your dataset
    
    model = create_model(num_layers, filter_size, dropout_rate, image_size, num_classes)
    model.summary()  # Display the model summary
    
    # Save the model configuration to a JSON file
    save_model_configuration(num_layers, filter_size, dropout_rate)
