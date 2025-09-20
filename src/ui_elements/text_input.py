import tkinter as tk
from tkinter import simpledialog

def user_input(prompt="Enter input: "):
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    user_input = simpledialog.askstring("Input", prompt)
    root.destroy()
    return user_input