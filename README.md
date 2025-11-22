🧮 Advanced BMI Calculator — Python Tkinter Project

A desktop BMI Calculator Application built using Python, Tkinter, SQLite, and Matplotlib.
This project allows users to calculate BMI, store their data, and view historical BMI trends in a clean, visual format.

📌 Features
✔ Modern Tkinter GUI

Clean, user-friendly layout

Easy-to-use input fields

Color-coded BMI results (Underweight, Healthy Weight, Overweight, Obesity)

✔ Multiple Height Units

Meters

Centimeters

Feet + Inches

✔ SQLite Database Integration

Stores your:

Username

Weight

Height

BMI value

BMI category

Timestamp

✔ BMI History Viewer

View previous BMI entries

Generate BMI trend graphs

Matplotlib chart embedded inside Tkinter

Auto-updates based on stored records

✔ Error Handling

Prevents invalid inputs

Displays helpful user-friendly messages

📂 Project Structure
📁 BMI-Calculator
   ├── BMI.py              # Main application
   ├── bmi_data.db         # SQLite database (auto-created if missing)
   └── README.md           # Project documentation

🛠 Technologies Used

Python 3

Tkinter (GUI framework)

SQLite3 (local database)

Matplotlib (graph plotting)

Datetime

▶️ How to Run the Application
1. Clone the repository
git clone https://github.com/<your-username>/BMI-Calculator.git
cd BMI-Calculator

2. Install required packages
pip install matplotlib

3. Run the program
python BMI.py


A new bmi_data.db file will be created automatically if it doesn’t already exist.

📉 BMI Categories Used
BMI Range	Category
< 18.5	Underweight
18.5 – 24.9	Healthy Weight
25 – 29.9	Overweight
≥ 30	Obesity

Each category is displayed with a unique color for clarity.
<img width="741" height="591" alt="image" src="https://github.com/user-attachments/assets/c7d618bf-7c55-446e-96a4-7baafedfa630" />

🤝 Contributing

Pull requests are welcome!
If you find a bug or want to improve the project, feel free to open an issue.
