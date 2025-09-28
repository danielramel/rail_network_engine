import tkinter as tk
from tkinter import messagebox

def alert(text="Alert!"):
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    messagebox.showinfo("Alert", text)
    root.destroy()