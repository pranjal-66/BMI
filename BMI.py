import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt # type: ignore
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg # type: ignore

# ============================================================
# DATABASE SETUP
# ============================================================

conn = sqlite3.connect("bmi_data.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS bmi_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    weight REAL NOT NULL,
    height REAL NOT NULL,
    bmi REAL NOT NULL,
    category TEXT NOT NULL,
    date TEXT NOT NULL
)
""")
conn.commit()


# ============================================================
# BMI FUNCTIONS
# ============================================================

def calculate_bmi(weight, height):
    return weight / (height ** 2)


def bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 24.9:
        return "Normal weight"
    elif 25 <= bmi < 29.9:
        return "Overweight"
    else:
        return "Obesity"


def category_color(cat):
    colors = {
        "Underweight": "#e6cd11",   # pale yellow
        "Healthy Weight": "#42c740", # soft green
        "Overweight": "#e7520e",     # orange
        "Obesity": "#e57373"         # red
    }
    return colors.get(cat, "black")


# ============================================================
# GUI APPLICATION
# ============================================================

class BMICalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced BMI Calculator")
        self.root.geometry("600x450")
        self.root.configure(bg="#f5f6fa")

        self.style = ttk.Style()
        self.style.configure("TLabel", font=("Segoe UI", 12), background="#f5f6fa")
        self.style.configure("TButton", font=("Segoe UI", 12), padding=8)
        self.style.configure("TEntry", font=("Segoe UI", 12))

        self.create_widgets()

    # --------------------------------------------------------

    def create_widgets(self):
        title = ttk.Label(self.root, text="BMI Calculator", font=("Segoe UI", 20, "bold"))
        title.pack(pady=10)

        frame = ttk.Frame(self.root)
        frame.pack(pady=10)

        # Username
        ttk.Label(frame, text="Username:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.username_entry = ttk.Entry(frame, width=30)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        # Weight
        ttk.Label(frame, text="Weight (kg):").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.weight_entry = ttk.Entry(frame)
        self.weight_entry.grid(row=1, column=1, padx=5, pady=5)

        # Height Units
        ttk.Label(frame, text="Height Unit:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.height_unit = ttk.Combobox(frame, values=["Meters", "Centimeters", "Feet & Inches"], state="readonly", width=27)
        self.height_unit.grid(row=2, column=1, padx=5)
        self.height_unit.current(0)
        self.height_unit.bind("<<ComboboxSelected>>", self.update_height_fields)

        # Height Entry Fields
        self.height_frame = ttk.Frame(frame)
        self.height_frame.grid(row=3, column=1, pady=5)

        self.height_entry = ttk.Entry(self.height_frame, width=20)
        self.height_entry.grid(row=0, column=0)

        # Buttons
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Calculate BMI", command=self.calculate_and_save).grid(row=0, column=0, padx=10)
        ttk.Button(btn_frame, text="View History", command=self.view_history).grid(row=0, column=1, padx=10)

        # Result label
        self.result_label = ttk.Label(self.root, text="", font=("Segoe UI", 14))
        self.result_label.pack(pady=10)

    # --------------------------------------------------------
    # Switch height input forms
    # --------------------------------------------------------

    def update_height_fields(self, event=None):
        for widget in self.height_frame.winfo_children():
            widget.destroy()

        unit = self.height_unit.get()

        if unit == "Meters":
            self.height_entry = ttk.Entry(self.height_frame, width=20)
            self.height_entry.grid(row=0, column=0)

        elif unit == "Centimeters":
            self.height_entry = ttk.Entry(self.height_frame, width=20)
            self.height_entry.grid(row=0, column=0)

        else:  # Feet & Inches
            ttk.Label(self.height_frame, text="ft").grid(row=0, column=1, padx=5)
            ttk.Label(self.height_frame, text="in").grid(row=0, column=3, padx=5)

            self.feet_entry = ttk.Entry(self.height_frame, width=7)
            self.feet_entry.grid(row=0, column=0)

            self.inch_entry = ttk.Entry(self.height_frame, width=7)
            self.inch_entry.grid(row=0, column=2)

    # --------------------------------------------------------

    def calculate_and_save(self):
        try:
            username = self.username_entry.get().strip()
            weight = float(self.weight_entry.get())
            unit = self.height_unit.get()

            if not username:
                raise ValueError("Username cannot be empty")
            if unit == "Meters":
                height = float(self.height_entry.get())

            elif unit == "Centimeters":
                height = float(self.height_entry.get()) / 100

            else:  # Feet & Inches
                feet = float(self.feet_entry.get())
                inches = float(self.inch_entry.get())
                height = (feet * 12 + inches) * 0.0254
                
            if weight <= 0 or height <= 0:
                raise ValueError("Weight and height must be positive numbers")

            bmi = calculate_bmi(weight, height)
            category = bmi_category(bmi)
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            cursor.execute("""
                INSERT INTO bmi_records (username, weight, height, bmi, category, date)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (username, weight, height, bmi, category, date))
            conn.commit()

            self.result_label.config(
                text=f"BMI: {bmi:.2f}  |  Category: {category}",
                foreground="#2d3436"
            )

            # ➜ Apply color to result
            color = category_color(category)
            self.result_label.config(
                text=f"BMI: {bmi:.2f}  |  Category: {category}",
                foreground=color
            )

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # --------------------------------------------------------

    def view_history(self):
        history_window = tk.Toplevel(self.root)
        history_window.title("BMI History")
        history_window.geometry("700x500")
        history_window.configure(bg="#f5f6fa")

        ttk.Label(history_window, text="Username:", font=("Segoe UI", 12)).pack(pady=5)
        username_entry = ttk.Entry(history_window, width=30)
        username_entry.pack(pady=5)

        def load_history():
            username = username_entry.get().strip()
            if not username:
                messagebox.showerror("Error", "Please enter a username.")
                return

            cursor.execute("""
                SELECT date, bmi FROM bmi_records WHERE username=? ORDER BY date ASC
            """, (username,))
            records = cursor.fetchall()

            if not records:
                messagebox.showinfo("No Data", "No history found for this user.")
                return

            # Clear previous chart
            for widget in chart_frame.winfo_children():
                widget.destroy()

            dates = [r[0] for r in records]
            bmi_values = [r[1] for r in records]

            fig, ax = plt.subplots(figsize=(6, 3))
            ax.plot(dates, bmi_values, marker="o")
            ax.set_title("BMI Trend Over Time")
            ax.set_xlabel("Date")
            ax.set_ylabel("BMI")
            ax.tick_params(axis='x', rotation=45)

            canvas = FigureCanvasTkAgg(fig, master=chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack()

        ttk.Button(history_window, text="Load History", command=load_history).pack(pady=10)

        chart_frame = ttk.Frame(history_window)
        chart_frame.pack(fill="both", expand=True, pady=10)


# ============================================================
# RUN APPLICATION
# ============================================================

root = tk.Tk()
app = BMICalculator(root)
root.mainloop()
