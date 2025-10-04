import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox

def user_input(prompt="Enter input: "):
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    user_input = simpledialog.askstring("Input", prompt)
    root.destroy()
    return user_input


def alert(title="Alert!", text="This is an alert"):
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    messagebox.showinfo(title, text)
    root.destroy()