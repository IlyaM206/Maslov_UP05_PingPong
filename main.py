import tkinter as tk
from typing import Final
from PIL import Image, ImageTk
from pathlib import Path
from game import PongGame

class StartMenu:
    IMAGE_BACKGROUND: Final[Path] = Path("images/menu.jpg")
    IMAGE_START: Final[Path] = Path("images/start.png")
    IMAGE_EXIT: Final[Path] = Path("images/exitgame.png")
    def __init__(self, root):
        self.root = root
        self.root.title("Пинг-Понг")
        self.w, self.h = 1280, 720
        sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()
        x, y = (sw - self.w)//2, (sh - self.h)//2
        self.root.geometry(f"{self.w}x{self.h}+{x}+{y}")
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(root, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # фоновое изображение
        self.bg_img = ImageTk.PhotoImage(
            Image.open(self.IMAGE_BACKGROUND).resize((1280,720), Image.Resampling.LANCZOS)
        )
        self.canvas.create_image(0, 0, image=self.bg_img, anchor="nw")
        # кнопка "Играть"
        self.start_img = ImageTk.PhotoImage(Image.open("images/startbut.png").resize((500,200), Image.Resampling.LANCZOS))

        btn = tk.Button(
            self.canvas,
            image=self.start_img,
            command=self.start_game,
            cursor="hand2"
        )
        btn.place(relx=0.5, rely=0.5, anchor="center")

        # кнопка выхода
        exit_btn = tk.Button(self.canvas, text="ВЫХОД", font=("Arial", 14), bg="#F44336", fg="white",
                             command=root.quit, cursor="hand2", width=8)
        exit_btn.place(x=self.w - 100, y=self.h - 50)