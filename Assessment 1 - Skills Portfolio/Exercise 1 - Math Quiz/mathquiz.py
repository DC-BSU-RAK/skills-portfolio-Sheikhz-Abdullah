import tkinter as tk
from tkinter import ttk, messagebox
import random
import time

# ---------------------------
# Math Quiz Application
# ---------------------------

# Theme / Colors
WINDOW_W, WINDOW_H = 900, 620
CARD_W = 680
CARD_H = 360

PALETTE = {
    "bg": "#0f1724",               # Page Background (Dark Navy)
    "card": "#0b1220",             # Card Background (Slightly Lighter)
    "muted": "#9aa6b2",            # Muted Text
    "accent": "#40C9A2",           # Primary Accent (Mint)
    "accent2": "#7A5FFF",          # Secondary Accent (Violet)
    "danger": "#FF6B6B",
    "white": "#ffffff",
    "soft": "#0f2533"              # Subtle Panel Color
}

FONT_TITLE = ("Segoe UI Semibold", 20)
FONT_SUB = ("Segoe UI", 12)
FONT_QUESTION = ("Segoe UI Variable", 28, "bold")
FONT_BUTTON = ("Segoe UI", 12, "bold")

MAX_QUESTIONS = 10

# ---------------------------
# Utility: Rounded Rectangle
# ---------------------------
def _round_rect(canvas, x1, y1, x2, y2, r=24, **kwargs):
    """Draw a rounded rectangle on a canvas and return the id"""
    points = [
        x1 + r, y1,
        x2 - r, y1,
        x2, y1,
        x2, y1 + r,
        x2, y2 - r,
        x2, y2,
        x2 - r, y2,
        x1 + r, y2,
        x1, y2,
        x1, y2 - r,
        x1, y1 + r,
        x1, y1
    ]
    return canvas.create_polygon(points, smooth=True, **kwargs)

# ---------------------------
# Main Application Class
# ---------------------------
class MathQuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Math Quiz")
        self.root.geometry(f"{WINDOW_W}x{WINDOW_H}")
        self.root.configure(bg=PALETTE["bg"])
        self.root.resizable(False, False)

        # quiz state
        self.difficulty = None
        self.current_q = 0
        self.attempt = 1
        self.score = 0
        self.num1 = 0
        self.num2 = 0
        self.operation = "+"
        self.max_q = MAX_QUESTIONS

        # styles
        self.style = ttk.Style(self.root)
        self.style.theme_use("clam")
        self.style.configure("TProgressbar", troughcolor=PALETTE["soft"], background=PALETTE["accent2"], thickness=14)
        self.style.configure("Round.TButton", borderwidth=0, focusthickness=0)

        # build menu screen by default
        self._build_menu()

# -----------------------
    # Screen: Menu
    # -----------------------
    def _build_menu(self):
        self._clear_root()
        canvas = tk.Canvas(self.root, width=WINDOW_W, height=WINDOW_H, highlightthickness=0, bg=PALETTE["bg"])
        canvas.pack(fill="both", expand=True)

        # Title
        canvas.create_text(WINDOW_W//2, 80, text="Math Quiz — Sharpen Your Skills", font=("Segoe UI Semibold", 32),
                           fill=PALETTE["white"])

        # Subtext
        canvas.create_text(WINDOW_W//2, 120, text="Pick a difficulty to begin (10 questions).",
                           font=FONT_SUB, fill=PALETTE["muted"])

        # Center card
        cx, cy = WINDOW_W//2, 330
        card_x1 = cx - CARD_W//2
        card_y1 = cy - CARD_H//2
        card_x2 = cx + CARD_W//2
        card_y2 = cy + CARD_H//2

        _round_rect(canvas, card_x1, card_y1, card_x2, card_y2, r=28, fill=PALETTE["card"], outline="")

        # Buttons row
        btn_w = 200
        spacing = 25
        start_x = cx - (btn_w*3 + spacing*2)/2 + btn_w/2

        self._create_glow_button(canvas, start_x, cy, "Easy", lambda: self._start_quiz("easy"), btn_w, 56, accent=PALETTE["accent"])
        self._create_glow_button(canvas, start_x + (btn_w + spacing), cy, "Moderate", lambda: self._start_quiz("moderate"), btn_w, 56, accent=PALETTE["accent2"])
        self._create_glow_button(canvas, start_x + 2*(btn_w + spacing), cy, "Advanced", lambda: self._start_quiz("advanced"), btn_w, 56, accent=PALETTE["danger"])

        # footer small note
        canvas.create_text(WINDOW_W//2, WINDOW_H - 30, text="Professional Build • Clean Layout • Educational Focus",
                           font=FONT_SUB, fill=PALETTE["muted"])

# ---------------------------
# Run The Application
# ---------------------------
if __name__ == "__main__":
    root = tk.Tk()
    # Avoid duplication by passing a single root object into the app
    app = MathQuizApp(root)
    root.mainloop()