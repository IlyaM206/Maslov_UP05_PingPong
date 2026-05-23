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

        # Параметры игры (упрощенные)
        self.pw, self.ph = 20, 120  # ракетка
        self.ball_size = 20
        self.margin = 40
        self.speed = 8
        self.win_score = 5

        # Позиции игроков
        self.player1_y = self.h // 2 - self.ph // 2
        self.player2_y = self.h // 2 - self.ph // 2
        self.score1 = self.score2 = 0
        self.game_over = False

        # Управление
        self.keys = {}

        # Мяч
        self.ball = {
            "x": self.w // 2,
            "y": self.h // 2,
            "dx": random.choice([-5, 5]),
            "dy": random.uniform(-3, 3)
        }

        # Загружаем фон (если файл существует)
        try:
            bg_image = Image.open("images/fongame.jpg").resize((width, height), Image.Resampling.LANCZOS)
            self.bg_img = ImageTk.PhotoImage(bg_image)
            self.canvas.create_image(0, 0, image=self.bg_img, anchor="nw")
        except Exception():
            # Если фона нет, просто заливаем Canvas темным цветом
            self.canvas.config(bg='#1a1a2e')

        self.setup_binds()
        self.update()

    def setup_binds(self):
        self.root.bind("<KeyPress-w>", lambda e: self.key_press("w", True))
        self.root.bind("<KeyRelease-w>", lambda e: self.key_press("w", False))
        self.root.bind("<KeyPress-s>", lambda e: self.key_press("s", True))
        self.root.bind("<KeyRelease-s>", lambda e: self.key_press("s", False))
        self.root.bind("<KeyPress-Up>", lambda e: self.key_press("up", True))
        self.root.bind("<KeyRelease-Up>", lambda e: self.key_press("up", False))
        self.root.bind("<KeyPress-Down>", lambda e: self.key_press("down", True))
        self.root.bind("<KeyRelease-Down>", lambda e: self.key_press("down", False))
        self.root.bind("<Escape>", self.quit_to_menu)

    def key_press(self, key, pressed):
        self.keys[key] = pressed

    def quit_to_menu(self, event = None):
        if messagebox.askyesno("Выход", "Выйти в меню?"):
            self.canvas.destroy()
            from main import StartMenu
            StartMenu(self.root)

    def move_paddles(self):
        if self.keys.get("w"):
            self.player1_y = max(0, self.player1_y - self.speed)
        if self.keys.get("s"):
            self.player1_y = min(self.h - self.ph, self.player1_y + self.speed)
        if self.keys.get("up"):
            self.player2_y = max(0, self.player2_y - self.speed)
        if self.keys.get("down"):
            self.player2_y = min(self.h - self.ph, self.player2_y + self.speed)

    def update_ball(self):
        if self.game_over:
            return

        self.ball["x"] += self.ball["dx"]
        self.ball["y"] += self.ball["dy"]

        # Отскок от верха/низа
        if self.ball["y"] <= self.ball_size // 2 or self.ball["y"] >= self.h - self.ball_size // 2:
            self.ball["dy"] = -self.ball["dy"]

        # Границы мяча
        left = self.ball["x"] - self.ball_size // 2
        right = self.ball["x"] + self.ball_size // 2
        top = self.ball["y"] - self.ball_size // 2
        bottom = self.ball["y"] + self.ball_size // 2

        # Левая ракетка
        if left <= self.margin + self.pw and right >= self.margin and \
                bottom >= self.player1_y and top <= self.player1_y + self.ph:
            self.ball["dx"] = abs(self.ball["dx"]) * 1.05
            offset = (self.ball["y"] - (self.player1_y + self.ph / 2)) / (self.ph / 2)
            self.ball["dy"] = offset * 5

        # Правая ракетка
        if right >= self.w - self.margin - self.pw and left <= self.w - self.margin and \
                bottom >= self.player2_y and top <= self.player2_y + self.ph:
            self.ball["dx"] = -abs(self.ball["dx"]) * 1.05
            offset = (self.ball["y"] - (self.player2_y + self.ph / 2)) / (self.ph / 2)
            self.ball["dy"] = offset * 5

        # Голы
        if self.ball["x"] < 0:
            self.score2 += 1
            self.reset_ball()
        elif self.ball["x"] > self.w:
            self.score1 += 1
            self.reset_ball()

        # Проверка победы
        if self.score1 >= self.win_score or self.score2 >= self.win_score:
            self.game_over = True

    def reset_ball(self):
        self.ball["x"] = self.w // 2
        self.ball["y"] = self.h // 2
        self.ball["dx"] = random.choice([-5, 5])
        self.ball["dy"] = random.uniform(-3, 3)

    def draw(self):
        self.canvas.delete("all")

        # Рисуем фон заново (если есть)
        if hasattr(self, 'bg_img'):
            self.canvas.create_image(0, 0, image=self.bg_img, anchor="nw")
        else:
            self.canvas.config(bg='#1a1a2e')

        # Центральная линия
        for i in range(0, self.h, 40):
            self.canvas.create_line(self.w // 2, i, self.w // 2, i + 20, fill="#333", width=3, dash=(15, 10))

        # Ракетки
        self.canvas.create_rectangle(self.margin, self.player1_y, self.margin + self.pw, self.player1_y + self.ph,
                                     fill="#8f02fe", outline="white", width=2)
        self.canvas.create_rectangle(self.w - self.margin - self.pw, self.player2_y, self.w - self.margin,
                                     self.player2_y + self.ph,
                                     fill="#00d25c", outline="white", width=2)

        # Мяч
        self.canvas.create_oval(self.ball["x"] - self.ball_size // 2, self.ball["y"] - self.ball_size // 2,
                                self.ball["x"] + self.ball_size // 2, self.ball["y"] + self.ball_size // 2,
                                fill="white", outline="#FFD700", width=2)

        # Счет
        self.canvas.create_text(self.w // 2, 40, text=f"{self.score1}  -  {self.score2}",
                                fill="white", font=("Arial", 36, "bold"))
