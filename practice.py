import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import csv

root = tk.Tk()
root.title("Crohn's symptom tracker")

tk.Label(root, text = "pain (0-10):").grid(row = 0, column = 0)
pain_entry = tk.Entry(root)
pain_entry.grid(row = 0, column = 1)

tk.Label(root, text = "fatigue (0-10):").grid(row = 1, column = 0)
fatigue_entry = tk.Entry(root)
fatigue_entry.grid(row = 1, column = 1)

tk.Label(root, text = "Diarrhea today? (yes/no):").grid(row = 2, column = 0)
diarrhea_var = tk.StringVar(value = "no")
tk.OptionMenu(root, diarrhea_var, "yes", "no").grid(row = 2, column = 1)

tk.Label(root, text = "Medication today? (yes/no):").grid(row = 3, column = 0)
medication_var = tk.StringVar(value = "no")
tk.OptionMenu(root, medication_var, "yes", "no").grid(row = 3, column = 1)

tk.Label(root, text = "Stress Level(0-10):").grid(row = 4, column = 0)
stress_entry = tk.Entry(root)
stress_entry.grid(row = 4, column = 1)

tk.Label(root, text = "Blood in Stool today? (yes/no):").grid(row = 5, column = 0)
bloodinstool_var = tk.StringVar(value = "no")
tk.OptionMenu(root, bloodinstool_var, "yes", "no").grid(row = 5, column = 1)

tk.Label(root, text = "Weight Changes:").grid(row = 6, column = 0)
weightchange_entry = tk.Entry(root)
weightchange_entry.grid(row = 6, column = 1)

tk.Label(root, text = "Please write down if you have any other symptoms").grid(row = 7, column = 0)
notes_entry = tk.Text(root, height = 7, width = 30)
notes_entry.grid(row = 7, column = 1)


def save_data():
    date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    pain_input_str = pain_entry.get()
    fatigue_input_str = fatigue_entry.get()
    stress_input_str = stress_entry.get()
    weightchange_input_str = weightchange_entry.get()
    if (pain_input_str.strip() == "" or fatigue_input_str.strip() == ""):
        messagebox.showerror("Input Missing", "It must not be empty")
        return
    try:
        pain_input = int(pain_input_str)
        fatigue_input = int(fatigue_input_str)
    except ValueError:
        messagebox.showerror("Input error", "It must be integer")
        return
    
    if (stress_input_str.strip() == "" or weightchange_input_str.strip() == ""):
        messagebox.showerror("Input Missing", "It must not be empty")
        return 
    try:
        stress_input = int(stress_input_str)
    except ValueError:
        messagebox.showerror("Input error", "It must be integer")
        return
    try:
        weightchange_input = float(weightchange_input_str)
    except ValueError:
        messagebox.showerror("Invalid input", "please enter a number like +1.0 or -1.0")
        return



    diarrhea_input = diarrhea_var.get()
    medication_input = medication_var.get()
    bloodinstool_input = bloodinstool_var.get()
    notes_input = notes_entry.get("1.0", "end").strip()

    if not (0 <= pain_input <= 10 and 0 <= fatigue_input <= 10 and 0 <= stress_input <= 10):
        messagebox.showerror("Invalid Number", "Number must be between 0 and 10")
        return
    if (pain_input >= 8 or fatigue_input >= 7):
        messagebox.showwarning("Emergency", "Must see doctor")
    try:
        with open ("symptom.csv", "a", newline = "") as file:
            writer = csv.writer(file)

            writer.writerow([date, pain_input, fatigue_input, diarrhea_input, medication_input, stress_input, bloodinstool_input, weightchange_input, notes_input])
    except Exception as e:
        messagebox.showerror("Save error", f"failed to save: {e}")

    messagebox.showinfo("Success", "Symptom logged!")
    pain_entry.delete(0, tk.END)
    fatigue_entry.delete(0, tk.END)
    stress_entry.delete(0, tk.END)
    weightchange_entry.delete(0,tk.END)
    notes_entry.delete("1.0", tk.END)

tk.Button(root, text = "Save Entry", command = save_data).grid(row = 8, column = 0, columnspan = 2)
root.mainloop()

