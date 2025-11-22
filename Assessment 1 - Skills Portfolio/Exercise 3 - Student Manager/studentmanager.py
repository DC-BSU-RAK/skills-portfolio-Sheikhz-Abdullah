import tkinter as tk
from tkinter import ttk, messagebox
import statistics


# ------------------------------------------------------------
# Utility Functions
# ------------------------------------------------------------

def calculate_grade(percent):
    if percent >= 70:
        return "A"
    elif percent >= 60:
        return "B"
    elif percent >= 50:
        return "C"
    elif percent >= 40:
        return "D"
    return "F"

def load_students(filename="studentMarks.txt"):
    students = []
    try:
        with open(filename, "r") as file:
            count = int(file.readline().strip())

            for _ in range(count):
                line = file.readline().strip()
                if not line:
                    continue

                sid, name, c1, c2, c3, exam = line.split(",")

                c1, c2, c3 = int(c1), int(c2), int(c3)
                exam = int(exam)
                coursework_total = c1 + c2 + c3

                overall = (coursework_total + exam) / 160 * 100
                grade = calculate_grade(overall)

                students.append({
                    "id": int(sid),
                    "name": name,
                    "course": coursework_total,
                    "exam": exam,
                    "overall": overall,
                    "grade": grade
                })
        return students
    except:
        messagebox.showerror("Error", "Failed to load studentMarks.txt")
        return []


# ------------------------------------------------------------
# Main GUI Application
# ------------------------------------------------------------

class StudentManagerApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Student Manager Dashboard")
        self.root.geometry("1000x600")
        self.root.configure(bg="#0f1625")

        self.students = load_students()

        # ----- Layout -----
        self.create_sidebar()
        self.create_content_frame()

    # ------------------------------------------------------------
    # Sidebar menu
    # ------------------------------------------------------------
    def create_sidebar(self):
        self.sidebar = tk.Frame(self.root, bg="#101a33", width=200)
        self.sidebar.pack(side="left", fill="y")

        title = tk.Label(
            self.sidebar,
            text="Student Manager",
            fg="white",
            bg="#101a33",
            font=("Segoe UI", 16, "bold"),
            pady=20
        )
        title.pack()

        # Menu buttons
        menu_items = [
            ("Show All Students", self.show_all_students),
            ("Find Student", self.find_student),
            ("Top Performer", self.show_best_student),
            ("Needs Support", self.show_lowest_student)
        ]

        for text, cmd in menu_items:
            b = tk.Button(
                self.sidebar,
                text=text,
                font=("Segoe UI", 12),
                bg="#172443",
                fg="white",
                relief="flat",
                activebackground="#20335c",
                activeforeground="white",
                command=cmd,
                height=2,
                width=18
            )
            b.pack(pady=5)

    # ------------------------------------------------------------
    # Content area
    # ------------------------------------------------------------
    def create_content_frame(self):
        self.content = tk.Frame(self.root, bg="#0f1625")
        self.content.pack(side="right", expand=True, fill="both")

    # Utility to clear content area
    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    # ------------------------------------------------------------
    # 1. View all students
    # ------------------------------------------------------------
    def show_all_students(self):
        self.clear_content()

        title = tk.Label(
            self.content,
            text="All Student Records",
            fg="white",
            bg="#0f1625",
            font=("Segoe UI", 18, "bold"),
            pady=10
        )
        title.pack()

        # Scrollable frame
        container = tk.Frame(self.content, bg="#0f1625")
        canvas = tk.Canvas(container, bg="#0f1625", highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg="#0f1625")

        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        container.pack(fill="both", expand=True, pady=10)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Student cards
        for s in self.students:
            card = tk.Frame(scroll_frame, bg="#162238", padx=15, pady=10)
            card.pack(fill="x", pady=8, padx=20)

            tk.Label(card, text=f"{s['name']} ({s['id']})",
                     fg="white", bg="#162238", font=("Segoe UI", 14, "bold")).pack(anchor="w")

            tk.Label(card, text=f"Coursework: {s['course']} / 60",
                     fg="#b5c6e0", bg="#162238", font=("Segoe UI", 11)).pack(anchor="w")

            tk.Label(card, text=f"Exam Mark: {s['exam']} / 100",
                     fg="#b5c6e0", bg="#162238", font=("Segoe UI", 11)).pack(anchor="w")

            tk.Label(card, text=f"Overall: {s['overall']:.2f}%",
                     fg="white", bg="#162238", font=("Segoe UI", 11, "bold")).pack(anchor="w")

            tk.Label(card, text=f"Grade: {s['grade']}",
                     fg="#00d27f" if s['grade'] in ("A", "B") else "#ff6b6b",
                     bg="#162238", font=("Segoe UI", 12)).pack(anchor="w")

        # Summary
        avg = statistics.mean([s["overall"] for s in self.students])
        summary = tk.Label(
            self.content,
            text=f"Class Size: {len(self.students)} | Average Overall: {avg:.2f}%",
            fg="#c9d5eb",
            bg="#0f1625",
            font=("Segoe UI", 12),
            pady=8
        )
        summary.pack()

    # ------------------------------------------------------------
    # 2. Find a student
    # ------------------------------------------------------------
    def find_student(self):
        self.clear_content()

        tk.Label(
            self.content, text="Find Student",
            fg="white", bg="#0f1625", font=("Segoe UI", 18, "bold")
        ).pack(pady=10)

        search_frame = tk.Frame(self.content, bg="#0f1625")
        search_frame.pack(pady=20)

        tk.Label(
            search_frame, text="Enter Name or ID:",
            fg="#ccd5e0", bg="#0f1625", font=("Segoe UI", 12)
        ).grid(row=0, column=0, padx=10)

        entry = tk.Entry(search_frame, width=30, font=("Segoe UI", 12))
        entry.grid(row=0, column=1)

        def search():
            query = entry.get().strip().lower()
            for s in self.students:
                if query in s["name"].lower() or query == str(s["id"]):
                    self.display_student_card(s)
                    return
            messagebox.showinfo("Not Found", "No matching student found.")

        tk.Button(
            search_frame, text="Search", command=search,
            bg="#1f3c6b", fg="white", font=("Segoe UI", 12), relief="flat"
        ).grid(row=0, column=2, padx=10)

    # ------------------------------------------------------------
    # Individual card display
    # ------------------------------------------------------------
    def display_student_card(self, s):
        self.clear_content()

        card = tk.Frame(self.content, bg="#162238", padx=20, pady=20)
        card.pack(pady=30)

        tk.Label(card, text=f"{s['name']} ({s['id']})",
                 fg="white", bg="#162238", font=("Segoe UI", 18, "bold")).pack()

        tk.Label(card, text=f"Coursework: {s['course']} / 60",
                 fg="#b5c6e0", bg="#162238", font=("Segoe UI", 12)).pack(anchor="w")

        tk.Label(card, text=f"Exam Mark: {s['exam']} / 100",
                 fg="#b5c6e0", bg="#162238", font=("Segoe UI", 12)).pack(anchor="w")

        tk.Label(card, text=f"Overall: {s['overall']:.2f}%",
                 fg="white", bg="#162238", font=("Segoe UI", 13, "bold")).pack(anchor="w")

        tk.Label(card, text=f"Grade: {s['grade']}",
                 fg="#00d27f" if s['grade'] in ("A", "B") else "#ff6b6b",
                 bg="#162238", font=("Segoe UI", 14)).pack(anchor="w")

    # ------------------------------------------------------------
    # 3. Highest scoring student
    # ------------------------------------------------------------
    def show_best_student(self):
        best = max(self.students, key=lambda x: x["overall"])
        self.display_student_card(best)

    # ------------------------------------------------------------
    # 4. Lowest scoring student
    # ------------------------------------------------------------
    def show_lowest_student(self):
        low = min(self.students, key=lambda x: x["overall"])
        self.display_student_card(low)

# ------------------------------------------------------------
# Run Application
# ------------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = StudentManagerApp(root)
    root.mainloop()