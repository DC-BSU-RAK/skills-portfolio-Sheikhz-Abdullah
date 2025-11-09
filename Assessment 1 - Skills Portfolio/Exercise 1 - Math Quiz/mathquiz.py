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