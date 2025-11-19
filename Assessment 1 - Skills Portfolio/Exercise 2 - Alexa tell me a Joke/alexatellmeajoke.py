import tkinter as tk
from tkinter import messagebox
import random, time, threading, winsound

class JokeApp:
    def __init__(self, root):
        self.root = root
        root.title("Alexa Tell Me A Joke")
        root.geometry("720x420")
        root.configure(bg="#101623")

        self.current_joke = ("", "")

        # Titles
        tk.Label(root, text="Alexa 🤖", fg="white", bg="#101623",
                 font=("Arial", 20, "bold")).pack(pady=45)
        tk.Label(root, text="Joke Assistant", fg="#C8B6FF", bg="#101623",
                 font=("Arial", 18, "bold")).pack()

        # Joke setup
        self.setup_lbl = tk.Label(root, text="Click 'New Joke' to start!",
                                  fg="white", bg="#101623", wraplength=600,
                                  font=("Arial", 15))
        self.setup_lbl.pack(pady=18)

        # Punchline
        self.punch_lbl = tk.Label(root, text="", fg="#9FE2F7", bg="#101623",
                                  wraplength=600, font=("Arial", 14, "italic"))
        self.punch_lbl.pack()

        # Buttons
        btns = tk.Frame(root, bg="#101623")
        btns.pack(pady=20)

        tk.Button(btns, text="New Joke", width=12, command=self.load_joke,
                  bg="#2D394D", fg="white", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=10)
        tk.Button(btns, text="Show Punchline", width=15, command=self.show_punch,
                  bg="#415A77", fg="white", font=("Arial", 12, "bold")).grid(row=0, column=1, padx=10)
        tk.Button(btns, text="Quit", width=10, command=root.quit,
                  bg="#A4161A", fg="white", font=("Arial", 12, "bold")).grid(row=0, column=2, padx=10)

    def load_joke(self):
        try:
            with open("randomJokes.txt", "r", encoding="utf-8") as f:
                lines = [x.strip() for x in f if "?" in x]
            setup, punch = random.choice(lines).split("?", 1)
            self.current_joke = (setup + "?", punch.strip())
            self.punch_lbl.config(text="")
            self.type_text(self.setup_lbl, self.current_joke[0], 0.02)
        except Exception as e:
            messagebox.showerror("Error", f"Couldn't read jokes:\n{e}")

    def show_punch(self):
        if not self.current_joke[1]:
            self.punch_lbl.config(text="Load a joke first!")
            return
        threading.Thread(target=self.play_sound).start()
        self.type_text(self.punch_lbl, self.current_joke[1], 0.03)

    def type_text(self, widget, text, delay):
        widget.config(text="")
        def run():
            out = ""
            for ch in text:
                out += ch
                widget.config(text=out)
                time.sleep(delay)
        threading.Thread(target=run).start()

    def play_sound(self):
        try:
            winsound.Beep(850, 120)
        except:
            pass

if __name__ == "__main__":
    JokeApp(tk.Tk())
    tk.mainloop()