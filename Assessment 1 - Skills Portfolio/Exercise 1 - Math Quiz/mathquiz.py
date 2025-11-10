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

    # -----------------------
    # Helper: glow button on canvas (rounded)
    # -----------------------
    def _create_glow_button(self, canvas, cx, cy, text, command, width=180, height=48, accent="#40C9A2"):
        left = cx - width/2
        right = cx + width/2
        top = cy - height/2
        bottom = cy + height/2
        # outer glow: slightly bigger rounded rectangle
        glow = _round_rect(canvas, left-3, top-3, right+3, bottom+3, r=20, fill="", outline="")
        canvas.itemconfigure(glow, fill=accent, stipple="gray50")
        # button rect
        rect = _round_rect(canvas, left, top, right, bottom, r=14, fill=PALETTE["soft"], outline="")
        # text
        txt = canvas.create_text(cx, cy, text=text, font=FONT_BUTTON, fill=PALETTE["white"])
        # bind area (use an invisible rect for events)
        area = canvas.create_rectangle(left, top, right, bottom, outline="", fill="")
        canvas.tag_bind(area, "<Enter>", lambda e: self._on_button_hover(canvas, rect, glow, txt, enter=True, accent=accent))
        canvas.tag_bind(area, "<Leave>", lambda e: self._on_button_hover(canvas, rect, glow, txt, enter=False, accent=accent))
        canvas.tag_bind(area, "<Button-1>", lambda e: (canvas.update(), command()))
        # also bind text & rect so clicks on them work
        for tag in (rect, txt):
            canvas.tag_bind(tag, "<Button-1>", lambda e: (canvas.update(), command()))
            canvas.tag_bind(tag, "<Enter>", lambda e: self._on_button_hover(canvas, rect, glow, txt, enter=True, accent=accent))
            canvas.tag_bind(tag, "<Leave>", lambda e: self._on_button_hover(canvas, rect, glow, txt, enter=False, accent=accent))

    def _on_button_hover(self, canvas, rect, glow, txt, enter, accent):
        if enter:
            canvas.itemconfigure(rect, fill=accent)
            canvas.itemconfigure(txt, fill="#0b1220")
            # highlight glow stronger
            canvas.itemconfigure(glow, stipple="")
        else:
            canvas.itemconfigure(rect, fill=PALETTE["soft"])
            canvas.itemconfigure(txt, fill=PALETTE["white"])
            canvas.itemconfigure(glow, stipple="gray50")

    # -----------------------
    # Start quiz
    # -----------------------
    def _start_quiz(self, level):
        self.difficulty = level
        self.current_q = 0
        self.attempt = 1
        self.score = 0
        self._build_quiz_screen()

    # -----------------------
    # Build Quiz Screen
    # -----------------------
    def _build_quiz_screen(self):
        self._clear_root()

        # top progress area
        top_frame = tk.Frame(self.root, bg=PALETTE["bg"])
        top_frame.pack(fill="x", pady=(18,6))

        title_lbl = tk.Label(top_frame, text="Math Quiz — Test Your Skills", bg=PALETTE["bg"], fg=PALETTE["white"], font=FONT_TITLE)
        title_lbl.pack(side="left", padx=26)

        self.score_lbl = tk.Label(top_frame, text=f"Score: {self.score}", bg=PALETTE["bg"], fg=PALETTE["muted"], font=FONT_SUB)
        self.score_lbl.pack(side="right", padx=26)

        # center card
        card_frame = tk.Frame(self.root, width=CARD_W, height=CARD_H, bg=PALETTE["card"])
        card_frame.pack(pady=18)
        card_frame.pack_propagate(False)

        # draw rounded card background using canvas for the polished look
        card_canvas = tk.Canvas(card_frame, width=CARD_W, height=CARD_H, bg=PALETTE["card"], highlightthickness=0)
        card_canvas.place(x=0, y=0)
        _round_rect(card_canvas, 0, 0, CARD_W, CARD_H, r=20, fill=PALETTE["card"], outline="")

        # question area
        q_area = tk.Frame(card_frame, bg=PALETTE["card"])
        q_area.place(relx=0.5, rely=0.18, anchor="n")

        self.q_label = tk.Label(q_area, text="", font=FONT_QUESTION, bg=PALETTE["card"], fg=PALETTE["white"])
        self.q_label.pack()

        # entry
        entry_frame = tk.Frame(card_frame, bg=PALETTE["card"])
        entry_frame.place(relx=0.5, rely=0.48, anchor="n")
        self.answer_var = tk.StringVar()
        self.answer_entry = tk.Entry(entry_frame, textvariable=self.answer_var, font=("Segoe UI", 20), width=8,
                                     justify="center", bd=0, highlightthickness=2, relief="flat", bg="#071018", fg=PALETTE["accent"], insertbackground="white")
        self.answer_entry.pack(ipady=10)
        self.answer_entry.bind("<Return>", lambda e: self._submit_answer())

        # submit button (rounded)
        btn_canvas = tk.Canvas(card_frame, width=180, height=56, bg=PALETTE["card"], highlightthickness=0)
        btn_canvas.place(relx=0.5, rely=0.70, anchor="n")
        bx1, by1, bx2, by2 = 0, 0, 180, 56
        _round_rect(btn_canvas, bx1, by1, bx2, by2, r=14, fill=PALETTE["accent"], outline="")
        btn_canvas.create_text(90, 28, text="Submit", font=FONT_BUTTON, fill="#0b1220")
        btn_canvas.bind("<Button-1>", lambda e: self._submit_answer())

        # progress / guidance area bottom of card
        bottom = tk.Frame(self.root, bg=PALETTE["bg"])
        bottom.pack(fill="x", pady=(6,18))
        # progress bar
        self.progress = ttk.Progressbar(bottom, orient="horizontal", mode="determinate", maximum=self.max_q, length=600)
        self.progress.pack(pady=6)
        # hint / attempt label
        self.hint_lbl = tk.Label(bottom, text="You have 2 attempts per question", bg=PALETTE["bg"], fg=PALETTE["muted"], font=FONT_SUB)
        self.hint_lbl.pack()

        # small control row
        ctrl = tk.Frame(self.root, bg=PALETTE["bg"])
        ctrl.pack(fill="x", pady=(8,0))
        tk.Button(ctrl, text="Quit", command=self._confirm_quit, bg=PALETTE["card"], fg=PALETTE["muted"], bd=0).pack(side="right", padx=26)

        # start first question
        self.root.after(120, self._next_question)    # small delay so UI renders first

    # -----------------------
    # Generate random ints based on difficulty
    # -----------------------
    def _rand_pair(self):
        if self.difficulty == "easy":
            return random.randint(1, 9), random.randint(1, 9)
        elif self.difficulty == "moderate":
            return random.randint(10, 99), random.randint(10, 99)
        else:
            return random.randint(1000, 9999), random.randint(1000, 9999)

    def _rand_op(self):
        return random.choice(["+", "-"])
    
    # -----------------------
    # Move to next question
    # -----------------------
    def _next_question(self):
        if self.current_q >= self.max_q:
            self._show_results()
            return
        self.current_q += 1
        self.attempt = 1
        self.answer_var.set("")
        self.answer_entry.focus_set()

        self.num1, self.num2 = self._rand_pair()
        self.operation = self._rand_op()

        self.q_label.config(text=f"{self.num1}  {self.operation}  {self.num2}  =")
        # animate small progress bump
        self._animate_progress(self.current_q)
        self._update_status_labels()

    # -----------------------
    # Submit answer logic
    # -----------------------
    def _submit_answer(self):
        text = self.answer_var.get().strip()
        if text == "":
            messagebox.showwarning("Input required", "Please enter an answer before submitting.")
            return
        # validate integer (allow negative)
        try:
            user = int(text)
        except ValueError:
            messagebox.showwarning("Invalid", "Please enter an integer (e.g. -5, 12).")
            return

        correct = self.num1 + self.num2 if self.operation == "+" else self.num1 - self.num2
        if user == correct:
            earned = 10 if self.attempt == 1 else 5
            self.score += earned
            self._show_correct_popup(earned)
            self._update_status_labels()
            # short delay then next
            self.root.after(650, self._next_question)
        else:
            if self.attempt == 1:
                self.attempt += 1
                self.hint_lbl.config(text="Incorrect — one more attempt!", fg=PALETTE["danger"])
                # keep on same question
            else:
                # reveal and move on
                messagebox.showinfo("Answer", f"Sorry — the correct answer was {correct}.")
                self.root.after(200, self._next_question)

    # -----------------------
    # Progress Animation
    # -----------------------
    def _animate_progress(self, target_value):
        start = self.progress["value"]
        end = target_value
        steps = 10
        delta = (end - start) / steps if steps else 0
        def step(i=0):
            if i >= steps:
                self.progress["value"] = end
                return
            self.progress["value"] = start + delta * (i+1)
            self.root.after(20, step, i+1)
        step()

    # -----------------------
    # Correct Popup Window (Fade Animation)
    # -----------------------
    def _show_correct_popup(self, earned):
        # small top-level window centered over root
        popup = tk.Toplevel(self.root)
        popup.overrideredirect(True)
        popup.configure(bg=PALETTE["card"])
        w, h = 320, 140
        x = self.root.winfo_x() + (WINDOW_W - w)//2
        y = self.root.winfo_y() + (WINDOW_H - h)//2
        popup.geometry(f"{w}x{h}+{x}+{y}")
        # rounded bg via canvas
        c = tk.Canvas(popup, width=w, height=h, highlightthickness=0, bg=PALETTE["card"])
        c.pack(fill="both", expand=True)
        _round_rect(c, 0, 0, w, h, r=18, fill=PALETTE["card"], outline="")

        # content
        c.create_text(w//2, 44, text="Correct!", font=("Segoe UI Semibold", 18), fill=PALETTE["accent2"])
        c.create_text(w//2, 84, text=f"+{earned} points", font=("Segoe UI", 14), fill=PALETTE["white"])

        # small check icon drawn (circle + tick)
        cx = w - 48
        cy = 48
        # circle
        c.create_oval(cx-22, cy-22, cx+22, cy+22, fill=PALETTE["accent"], outline="")
        # tick (approx)
        c.create_line(cx - 9, cy - 1, cx - 1, cy + 9, cx + 11, cy - 11,
              width=3.5, fill=PALETTE["card"], capstyle="round")

        # fade in effect (simulate by updating alpha if supported)
        try:
            popup.attributes("-alpha", 0.0)
            def fade(a=0.0):
                a += 0.08
                if a >= 1.0:
                    popup.attributes("-alpha", 1.0)
                    popup.after(650, popup.destroy)
                else:
                    popup.attributes("-alpha", a)
                    popup.after(25, fade, a)
            fade()
        except:
            # if platform doesn't support alpha changes
            popup.after(650, popup.destroy)

    # -----------------------
    # Update Score / Hint / Clue Labels
    # -----------------------
    def _update_status_labels(self):
        self.score_lbl.config(text=f"Score: {self.score}")
        self.hint_lbl.config(text=f"Question {self.current_q}/{self.max_q} — Attempts left: {2 - (self.attempt - 1)}",fg=PALETTE["muted"])

    # -----------------------
    # Final results screen
    # -----------------------
    def _show_results(self):
        self._clear_root()
        # big card
        frame = tk.Frame(self.root, bg=PALETTE["card"], width=760, height=420)
        frame.place(relx=0.5, rely=0.5, anchor="center")
        frame.pack_propagate(False)

        tk.Label(frame, text="Quiz Complete", font=("Segoe UI Semibold", 26), bg=PALETTE["card"], fg=PALETTE["accent2"]).pack(pady=(28,6))
        tk.Label(frame, text=f"Final Score: {self.score} / {self.max_q * 10}", font=("Segoe UI", 18), bg=PALETTE["card"], fg=PALETTE["white"]).pack(pady=6)

        rank = self._grade(self.score)
        tk.Label(frame, text=f"Grade: {rank}", font=("Segoe UI", 16), bg=PALETTE["card"], fg=PALETTE["muted"]).pack(pady=6)

        # trophy-like badge for A+
        if self.score >= 90:
            badge = tk.Label(frame, text="🏆 Math Champion", font=("Segoe UI Semibold", 16), bg=PALETTE["card"], fg=PALETTE["accent"])
            badge.pack(pady=8)

        btn_frame = tk.Frame(frame, bg=PALETTE["card"])
        btn_frame.pack(pady=16)
        tk.Button(btn_frame, text="Play Again", font=FONT_BUTTON, bg=PALETTE["accent"], fg="#051019", bd=0, command=self._build_menu).grid(row=0, column=0, padx=12)
        tk.Button(btn_frame, text="Exit", font=FONT_BUTTON, bg=PALETTE["danger"], fg="#fff", bd=0, command=self.root.destroy).grid(row=0, column=1, padx=12)

    def _grade(self, s):
        if s >= 90: return "A+"
        if s >= 75: return "A"
        if s >= 60: return "B"
        if s >= 40: return "C"
        return "F"

    # -----------------------
    # Confirm Quit
    # -----------------------
    def _confirm_quit(self):
        if messagebox.askyesno("Quit", "Are you sure you want to exit the quiz?"):
            self.root.destroy()

    # -----------------------
    # Clears The Root Children
    # -----------------------
    def _clear_root(self):
        for w in self.root.winfo_children():
            w.destroy()

# ---------------------------
# Run The Application
# ---------------------------
if __name__ == "__main__":
    root = tk.Tk()
    # Avoid duplication by passing a single root object into the app
    app = MathQuizApp(root)
    root.mainloop()