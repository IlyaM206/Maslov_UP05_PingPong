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