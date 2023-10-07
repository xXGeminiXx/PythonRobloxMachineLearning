import tkinter as tk

class ToolTip:
    """
    Create a tooltip for a Tkinter widget.

    Args:
        widget (tk.Widget): The widget for which the tooltip is created.
        text (str): The text to display in the tooltip.
        delay (int): The delay (in milliseconds) before the tooltip appears (default is 500ms).
        activation_event (str): The event that triggers the tooltip (default is "<Enter>").
        background (str): The background color of the tooltip (default is "white").

    Attributes:
        widget (tk.Widget): The widget for which the tooltip is created.
        text (str): The text to display in the tooltip.
        delay (int): The delay before the tooltip appears (in milliseconds).
        activation_event (str): The event that triggers the tooltip.
        tooltip (tk.Toplevel): The tooltip window.
    """
    
    def __init__(self, widget, text, delay=500, activation_event="<Enter>", background="white"):
        self.widget = widget
        self.text = text
        self.delay = delay
        self.activation_event = activation_event
        self.background = background
        self.tooltip = None
        self._entering_widget = False

        self.widget.bind(self.activation_event, self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        if not self._entering_widget:
            self.widget.after(self.delay, self._display_tooltip)

    def _display_tooltip(self):
        if not self.tooltip:
            x, y, _, _ = self.widget.bbox("insert")
            x += self.widget.winfo_rootx() + 25
            y += self.widget.winfo_rooty() + 25
            self.tooltip = tk.Toplevel(self.widget)
            self.tooltip.wm_overrideredirect(True)
            self.tooltip.wm_geometry(f"+{x}+{y}")
            label = tk.Label(
                self.tooltip,
                text=self.text,
                background=self.background,
                relief="solid",
                borderwidth=1,
                padx=5,
                pady=5,
                wraplength=200,
            )
            label.pack()
            self._entering_widget = True

    def hide_tooltip(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None
            self._entering_widget = False

# Example usage:
# root = tk.Tk()
# button = tk.Button(root, text="Hover me")
# button.pack()
# tooltip = ToolTip(button, "This is a tooltip.")
# root.mainloop()


def initialize_gui(root, status_var):
    # Main Frame
    main_frame = tk.Frame(root)
    main_frame.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)

    # Buttons
    select_area_button = tk.Button(main_frame, text="Select Screen Area", command=lambda: print('Button clicked'))
    reset_area_button = tk.Button(main_frame, text="Reset Screen Area",  command=lambda: print('Button clicked'))

    capture_button = tk.Button(main_frame, text="Capture on Click",  command=lambda: print('Button clicked'))
    batch_capture_button = tk.Button(main_frame, text="Batch Capture",  command=lambda: print('Button clicked'))
    train_model_button = tk.Button(main_frame, text="Train Model",  command=lambda: print('Button clicked'))

    select_area_button.pack(pady=5)
    reset_area_button.pack(pady=5)
    capture_button.pack(pady=5)
    batch_capture_button.pack(pady=5)
    train_model_button.pack(pady=5)

    # Status label
    status_label = tk.Label(main_frame, textvariable=status_var)
    status_label.pack(pady=10)
    return {
        'select_area_button': select_area_button,
        'reset_area_button': reset_area_button,
        'capture_button': capture_button,
        'batch_capture_button': batch_capture_button,
        'train_model_button': train_model_button,
        # ... add other necessary GUI elements as needed
    }
