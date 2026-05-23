import tkinter as tk
import random
from PIL import Image, ImageTk
from tkinter import messagebox


class PongGame:
    def __init__(self, root, width, height):
        self.root = root
        self.w, self.h = width, height
        self.root.geometry(f"{width}x{height}")
        self.root.resizable(False, False)

        # Создаем Canvas с черным фоном (на всякий случай)
        self.canvas = tk.Canvas(root, highlightthickness=0, bg='black')
        self.canvas.pack(fill="both", expand=True)