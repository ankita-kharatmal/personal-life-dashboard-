import tkinter as tk
import matplotlib.pyplot as plt
from datetime import datetime

# Save Data
def submit_data():
    study = study_entry.get()
    phone = phone_entry.get()
    mood = mood_var.get()

    if study == "" or phone == "":
        result_label.config(text="⚠️ Please enter all fields!")
        return

    try:
        study = float(study)
        phone = float(phone)
    except:
        result_label.config(text="⚠️ Enter valid numbers!")
        return

    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    with open("data.txt", "a") as file:
        file.write(f"{now},{study},{mood},{phone}\n")

    msg = f"Saved ✅ | Study: {study} | Phone: {phone} | Mood: {mood}"

    if phone > study:
        msg += "\n⚠️ Reduce phone usage!"

    result_label.config(text=msg)

    study_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)

# Show History
def show_history():
    try:
        with open("data.txt", "r") as file:
            data = file.readlines()

        if not data:
            history_label.config(text="No data found!")
            return

        formatted = ""
        for line in data:
            d, s, m, p = line.strip().split(",")
            formatted += f"{d} | Study: {s} | Phone: {p} | Mood: {m}\n"

        history_label.config(text=formatted)

    except:
        history_label.config(text="No data file found!")

# Show Graph
def show_graph():
    try:
        with open("data.txt", "r") as file:
            data = file.readlines()

        study = []
        phone = []

        for line in data:
            parts = line.strip().split(",")
            if len(parts) == 4:
                _, s, _, p = parts
                study.append(float(s))
                phone.append(float(p))

        if len(study) == 0:
            result_label.config(text="No valid data to show graph!")
            return

        plt.plot(study, label="Study Hours")
        plt.plot(phone, label="Phone Usage")

        plt.legend()
        plt.title("Study vs Phone Usage")
        plt.xlabel("Days")
        plt.ylabel("Hours")

        plt.show()

    except Exception as e:
        result_label.config(text="Error: " + str(e))

# UI
root = tk.Tk()
root.title("Personal Life Dashboard")
root.geometry("350x520")

tk.Label(root, text="Personal Life Dashboard", font=("Arial", 14, "bold")).pack(pady=10)

tk.Label(root, text="Enter Study Hours:").pack()
study_entry = tk.Entry(root)
study_entry.pack(pady=5)

tk.Label(root, text="Enter Phone Usage Hours:").pack()
phone_entry = tk.Entry(root)
phone_entry.pack(pady=5)

tk.Label(root, text="Select Mood:").pack()
mood_var = tk.StringVar()
mood_var.set("Happy")

tk.OptionMenu(root, mood_var, "Happy", "Sad", "Neutral").pack(pady=5)

tk.Button(root, text="Submit", command=submit_data).pack(pady=5)
tk.Button(root, text="Show History", command=show_history).pack(pady=5)
tk.Button(root, text="Show Graph", command=show_graph).pack(pady=5)

result_label = tk.Label(root, text="", fg="green")
result_label.pack(pady=10)

history_label = tk.Label(root, text="", justify="left")
history_label.pack()

root.mainloop()
