import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import statistics
import os

# ---------------------------
# Helper functions & file IO
# ---------------------------

def calculate_grade(percent):
    # Simple grade boundaries
    if percent >= 70:
        return "A"
    elif percent >= 60:
        return "B"
    elif percent >= 50:
        return "C"
    elif percent >= 40:
        return "D"
    return "F"

def data_file_path(filename="studentMarks.txt"):
    return os.path.join(os.path.dirname(__file__), filename)

def load_students(filename="studentMarks.txt"):
    filepath = data_file_path(filename)
    students = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            first = f.readline()
            if not first:
                return []
            try:
                count = int(first.strip())
            except:
                # Fallback: treat first line as a record if count malformed
                # (but your file is in the correct format, so this is defensive)
                f.seek(0)
                lines = [l.strip() for l in f if l.strip()]
                for line in lines:
                    parts = line.split(",")
                    if len(parts) >= 6:
                        sid, name, c1, c2, c3, exam = parts[:6]
                        c1, c2, c3 = int(c1), int(c2), int(c3)
                        exam = int(exam)
                        coursework_total = c1 + c2 + c3
                        overall = (coursework_total + exam) / 160 * 100
                        students.append({
                            "id": int(sid),
                            "name": name,
                            "c1": c1,
                            "c2": c2,
                            "c3": c3,
                            "course": coursework_total,
                            "exam": exam,
                            "overall": overall,
                            "grade": calculate_grade(overall)
                        })
                return students

            # Normal path: read exactly 'count' lines (but also safely iterate if file shorter/longer)
            for _ in range(count):
                line = f.readline()
                if not line:
                    break
                line = line.strip()
                if not line:
                    continue
                parts = line.split(",")
                if len(parts) < 6:
                    continue
                sid, name, c1, c2, c3, exam = parts[:6]
                try:
                    c1, c2, c3 = int(c1), int(c2), int(c3)
                    exam = int(exam)
                except:
                    # Skip malformed record
                    continue
                coursework_total = c1 + c2 + c3
                overall = (coursework_total + exam) / 160 * 100
                students.append({
                    "id": int(sid),
                    "name": name,
                    "c1": c1,
                    "c2": c2,
                    "c3": c3,
                    "course": coursework_total,
                    "exam": exam,
                    "overall": overall,
                    "grade": calculate_grade(overall)
                })
        return students
    except FileNotFoundError:
        messagebox.showerror("File Missing", f"Student file not found: {filepath}")
        return []
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load file: {filepath}\n{e}")
        return []

def save_students(students, filename="studentMarks.txt"):
    filepath = data_file_path(filename)
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(str(len(students)) + "\n")
            for s in students:
                # Ensure fields c1,c2,c3 and exam exist
                c1 = int(s.get("c1", 0))
                c2 = int(s.get("c2", 0))
                c3 = int(s.get("c3", 0))
                exam = int(s.get("exam", 0))
                f.write(f"{s['id']},{s['name']},{c1},{c2},{c3},{exam}\n")
    except Exception as e:
        messagebox.showerror("Save Error", f"Failed to save students to file:\n{e}")

def recalc_student_fields(s):
    s["c1"] = int(s.get("c1", 0))
    s["c2"] = int(s.get("c2", 0))
    s["c3"] = int(s.get("c3", 0))
    s["exam"] = int(s.get("exam", 0))
    s["course"] = s["c1"] + s["c2"] + s["c3"]
    s["overall"] = (s["course"] + s["exam"]) / 160 * 100
    s["grade"] = calculate_grade(s["overall"])

# ---------------------------
# GUI application
# ---------------------------

class StudentManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Manager Dashboard")
        self.root.geometry("1000x620")
        self.root.configure(bg="#0f1625")

        # Load data
        self.students = load_students()

        # UI
        self.create_sidebar()
        self.create_content_frame()

    # Sidebar (menu)
    def create_sidebar(self):
        self.sidebar = tk.Frame(self.root, bg="#101a33", width=220)
        self.sidebar.pack(side="left", fill="y")

        title = tk.Label(self.sidebar, text="Student Manager",
                         fg="white", bg="#101a33", font=("Segoe UI", 16, "bold"),
                         pady=18)
        title.pack()

        menu_items = [
            ("Show All Students", self.show_all_students),
            ("Find Student", self.find_student),
            ("Top Performer", self.show_best_student),
            ("Needs Support", self.show_lowest_student),
            ("Sort Records", self.sort_records),
            ("Add Student", self.add_student),
            ("Delete Student", self.delete_student),
            ("Update Student", self.update_student),
        ]

        for text, cmd in menu_items:
            b = tk.Button(self.sidebar, text=text, font=("Segoe UI", 11),
                          bg="#172443", fg="white", relief="flat",
                          activebackground="#20335c", activeforeground="white",
                          command=cmd, height=2, width=20)
            b.pack(pady=6)

    # Main content
    def create_content_frame(self):
        self.content = tk.Frame(self.root, bg="#0f1625")
        self.content.pack(side="right", expand=True, fill="both")

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    # ---------------------------
    # Display helpers
    # ---------------------------
    def display_students_list(self, students_list):
        self.clear_content()

        title = tk.Label(self.content, text="Student Records",
                         fg="white", bg="#0f1625", font=("Segoe UI", 18, "bold"),
                         pady=10)
        title.pack()

        container = tk.Frame(self.content, bg="#0f1625")
        canvas = tk.Canvas(container, bg="#0f1625", highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg="#0f1625")

        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas.create_window((0,0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        container.pack(fill="both", expand=True, pady=10)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for s in students_list:
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
        if students_list:
            avg = statistics.mean([s["overall"] for s in students_list])
        else:
            avg = 0
        summary = tk.Label(self.content, text=f"Class Size: {len(students_list)} | Average Overall: {avg:.2f}%",
                           fg="#c9d5eb", bg="#0f1625", font=("Segoe UI", 12), pady=8)
        summary.pack()

    # ---------------------------
    # Main menu actions
    # ---------------------------
    def show_all_students(self):
        self.display_students_list(self.students)

    def find_student(self):
        self.clear_content()
        tk.Label(self.content, text="Find Student",
                 fg="white", bg="#0f1625", font=("Segoe UI", 18, "bold")).pack(pady=10)

        search_frame = tk.Frame(self.content, bg="#0f1625")
        search_frame.pack(pady=20)

        tk.Label(search_frame, text="Enter Name or ID:",
                 fg="#ccd5e0", bg="#0f1625", font=("Segoe UI", 12)).grid(row=0, column=0, padx=10)

        entry = tk.Entry(search_frame, width=30, font=("Segoe UI", 12))
        entry.grid(row=0, column=1)

        def search():
            query = entry.get().strip().lower()
            for s in self.students:
                if query == str(s["id"]) or query in s["name"].lower():
                    self.display_student_card(s)
                    return
            messagebox.showinfo("Not Found", "No matching student found.")

        tk.Button(search_frame, text="Search", command=search,
                  bg="#1f3c6b", fg="white", font=("Segoe UI", 12), relief="flat").grid(row=0, column=2, padx=10)

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

    def show_best_student(self):
        if not self.students:
            messagebox.showinfo("No Data", "No student records available.")
            return
        best = max(self.students, key=lambda x: x["overall"])
        self.display_student_card(best)

    def show_lowest_student(self):
        if not self.students:
            messagebox.showinfo("No Data", "No student records available.")
            return
        low = min(self.students, key=lambda x: x["overall"])
        self.display_student_card(low)

    # ---------------------------
    # 5. Sort student records
    # ---------------------------
    def sort_records(self):
        # Dialog to choose ascending or descending
        choice = messagebox.askquestion("Sort Order", "Sort by overall score ascending?\nChoose 'No' for descending.")
        if choice == "yes":
            sorted_list = sorted(self.students, key=lambda x: x["overall"], reverse=True)
        else:
            sorted_list = sorted(self.students, key=lambda x: x["overall"])
        self.display_students_list(sorted_list)

    # ---------------------------
    # 6. Add a student record
    # ---------------------------
    def add_student(self):
        self.clear_content()
        tk.Label(self.content, text="Add New Student", fg="white", bg="#0f1625",
                 font=("Segoe UI", 18, "bold")).pack(pady=10)

        form = tk.Frame(self.content, bg="#0f1625")
        form.pack(pady=10)

        labels = ["ID (integer):", "Full Name:", "Coursework 1 (0-20):", "Coursework 2 (0-20):",
                  "Coursework 3 (0-20):", "Exam (0-100):"]
        entries = []

        for i, lab in enumerate(labels):
            tk.Label(form, text=lab, fg="#ccd5e0", bg="#0f1625", font=("Segoe UI", 11)).grid(row=i, column=0, pady=6, padx=6, sticky="e")
            ent = tk.Entry(form, width=30, font=("Segoe UI", 11))
            ent.grid(row=i, column=1, pady=6, padx=6)
            entries.append(ent)

        # Pre-fill a new unique ID (max existing + 1)
        try:
            next_id = max([s["id"] for s in self.students]) + 1 if self.students else 1000
        except:
            next_id = 1000
        entries[0].insert(0, str(next_id))

        def do_add():
            try:
                sid = int(entries[0].get().strip())
                name = entries[1].get().strip()
                c1 = int(entries[2].get().strip())
                c2 = int(entries[3].get().strip())
                c3 = int(entries[4].get().strip())
                exam = int(entries[5].get().strip())
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter valid numeric values for ID, coursework and exam.")
                return

            if not name:
                messagebox.showerror("Invalid Input", "Name cannot be empty.")
                return

            # Validate ranges
            if not (0 <= c1 <= 20 and 0 <= c2 <= 20 and 0 <= c3 <= 20 and 0 <= exam <= 100):
                messagebox.showerror("Invalid Range", "Coursework must be 0-20 each; exam must be 0-100.")
                return

            # Prevent duplicate IDs
            if any(s["id"] == sid for s in self.students):
                messagebox.showerror("Duplicate ID", f"A student with ID {sid} already exists.")
                return

            new_student = {"id": sid, "name": name, "c1": c1, "c2": c2, "c3": c3, "exam": exam}
            recalc_student_fields(new_student)
            self.students.append(new_student)
            save_students(self.students)
            messagebox.showinfo("Added", f"Student {name} added.")
            self.show_all_students()

        tk.Button(form, text="Add Student", command=do_add, bg="#1f6fb2", fg="white", font=("Segoe UI", 12), relief="flat").grid(row=len(labels), column=0, columnspan=2, pady=12)

    # ---------------------------
    # 7. Delete a student record
    # ---------------------------
    def delete_student(self):
        self.clear_content()
        tk.Label(self.content, text="Delete Student", fg="white", bg="#0f1625", font=("Segoe UI", 18, "bold")).pack(pady=10)

        frame = tk.Frame(self.content, bg="#0f1625")
        frame.pack(pady=16)

        tk.Label(frame, text="Enter Student ID or Full Name:", fg="#ccd5e0", bg="#0f1625", font=("Segoe UI", 12)).grid(row=0, column=0, padx=8)
        entry = tk.Entry(frame, width=30, font=("Segoe UI", 12))
        entry.grid(row=0, column=1, padx=8)

        def do_delete():
            key = entry.get().strip()
            if not key:
                messagebox.showerror("Input Needed", "Please enter an ID or full name.")
                return
            # Try ID first
            to_remove = None
            try:
                kid = int(key)
                for s in self.students:
                    if s["id"] == kid:
                        to_remove = s
                        break
            except:
                # search by name (case-insensitive substring)
                matches = [s for s in self.students if key.lower() in s["name"].lower()]
                if len(matches) == 0:
                    to_remove = None
                elif len(matches) == 1:
                    to_remove = matches[0]
                else:
                    # Multiple matches: ask user to choose by ID
                    ids = ", ".join(f"{m['id']}:{m['name']}" for m in matches)
                    messagebox.showinfo("Multiple Matches", f"Multiple students match:\n{ids}\nPlease enter the ID to delete.")
                    return

            if not to_remove:
                messagebox.showinfo("Not Found", "No matching student found.")
                return

            confirm = messagebox.askyesno("Confirm Delete", f"Delete {to_remove['name']} ({to_remove['id']})?")
            if not confirm:
                return

            self.students = [s for s in self.students if s["id"] != to_remove["id"]]
            save_students(self.students)
            messagebox.showinfo("Deleted", f"Student {to_remove['name']} removed.")
            self.show_all_students()

        tk.Button(frame, text="Delete", command=do_delete, bg="#c62828", fg="white", font=("Segoe UI", 12), relief="flat").grid(row=1, column=0, columnspan=2, pady=12)

    # ---------------------------
    # 8. Update a student's record
    # ---------------------------
    def update_student(self):
        self.clear_content()
        tk.Label(self.content, text="Update Student Record", fg="white", bg="#0f1625", font=("Segoe UI", 18, "bold")).pack(pady=10)

        top = tk.Frame(self.content, bg="#0f1625")
        top.pack(pady=8)
        tk.Label(top, text="Enter ID or Full Name to find:", fg="#ccd5e0", bg="#0f1625", font=("Segoe UI", 12)).grid(row=0, column=0, padx=6)
        entry = tk.Entry(top, width=30, font=("Segoe UI", 12))
        entry.grid(row=0, column=1, padx=6)

        def find_and_edit():
            key = entry.get().strip()
            if not key:
                messagebox.showerror("Input Needed", "Please enter a name or an ID to search.")
                return
            found = None
            try:
                kid = int(key)
                for s in self.students:
                    if s["id"] == kid:
                        found = s
                        break
            except:
                # name match (case-insensitive substring)
                matches = [s for s in self.students if key.lower() in s["name"].lower()]
                if len(matches) == 0:
                    found = None
                elif len(matches) == 1:
                    found = matches[0]
                else:
                    # multiple matches -> ask for ID
                    ids = ", ".join(f"{m['id']}:{m['name']}" for m in matches)
                    messagebox.showinfo("Multiple Matches", f"Multiple students match:\n{ids}\nPlease enter the ID to update.")
                    return

            if not found:
                messagebox.showinfo("Not Found", "No matching student found.")
                return

            # Show edit form for the found student
            self._show_update_form(found)

        tk.Button(top, text="Find", command=find_and_edit, bg="#1f3c6b", fg="white", font=("Segoe UI", 12), relief="flat").grid(row=0, column=2, padx=8)

    def _show_update_form(self, student):
        self.clear_content()
        tk.Label(self.content, text=f"Updating: {student['name']} ({student['id']})",
                 fg="white", bg="#0f1625", font=("Segoe UI", 16, "bold")).pack(pady=10)

        form = tk.Frame(self.content, bg="#0f1625")
        form.pack(pady=6)

        labels = ["Full Name:", "Coursework 1 (0-20):", "Coursework 2 (0-20):",
                  "Coursework 3 (0-20):", "Exam (0-100):"]
        entries = []

        # Pre-fill values
        initial = [student.get("name", ""), student.get("c1", 0), student.get("c2", 0), student.get("c3", 0), student.get("exam", 0)]

        for i, lab in enumerate(labels):
            tk.Label(form, text=lab, fg="#ccd5e0", bg="#0f1625", font=("Segoe UI", 11)).grid(row=i, column=0, pady=6, padx=6, sticky="e")
            ent = tk.Entry(form, width=30, font=("Segoe UI", 11))
            ent.grid(row=i, column=1, pady=6, padx=6)
            ent.insert(0, str(initial[i]))
            entries.append(ent)

        def do_update():
            name = entries[0].get().strip()
            try:
                c1 = int(entries[1].get().strip())
                c2 = int(entries[2].get().strip())
                c3 = int(entries[3].get().strip())
                exam = int(entries[4].get().strip())
            except ValueError:
                messagebox.showerror("Invalid Input", "For the coursework and exam, please enter valid numeric values.")
                return

            if not name:
                messagebox.showerror("Invalid Input", "Name feild cannot be empty.")
                return
            if not (0 <= c1 <= 20 and 0 <= c2 <= 20 and 0 <= c3 <= 20 and 0 <= exam <= 100):
                messagebox.showerror("Invalid Range", "Coursework must be from 0-20 each and exam must be from 0-100.")
                return

            # Apply changes
            student["name"] = name
            student["c1"] = c1
            student["c2"] = c2
            student["c3"] = c3
            student["exam"] = exam
            recalc_student_fields(student)
            save_students(self.students)
            messagebox.showinfo("Updated", f"Student {student['name']} updated.")
            self.show_all_students()

        tk.Button(form, text="Save Changes", command=do_update, bg="#1f6fb2", fg="white", font=("Segoe UI", 12), relief="flat").grid(row=len(labels), column=0, columnspan=2, pady=12)

# ---------------------------
# Start application
# ---------------------------

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentManagerApp(root)
    root.mainloop()