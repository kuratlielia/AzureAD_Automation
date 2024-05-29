import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd

class CSVEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV Editor")
        self.filepath = None
        self.data = None
        self.entries = []

        self.load_button = tk.Button(root, text="CSV Laden", command=self.load_csv, bg='#007bff', fg='white', font=('Arial', 12, 'bold'), relief='raised', bd=5)
        self.load_button.pack(pady=20)

        self.table_frame = tk.Frame(root)
        self.table_frame.pack(pady=20)

        self.save_button = tk.Button(root, text="Änderungen speichern", command=self.save_changes, bg='#28a745', fg='white', font=('Arial', 12, 'bold'), relief='raised', bd=5)
        self.save_button.pack(pady=20)

        self.reset_button = tk.Button(root, text="Alle auf False setzen", command=self.set_all_false, bg='#dc3545', fg='white', font=('Arial', 12, 'bold'), relief='raised', bd=5)
        self.reset_button.pack(pady=20)
        self.reset_button.pack_forget()  # Initially hide the reset button

    def load_csv(self):
        self.filepath = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if self.filepath:
            self.data = pd.read_csv(self.filepath)
            self.show_table()
            self.adjust_window_size()
            self.reset_button.pack(pady=20)  # Show the reset button after loading the CSV

    def show_table(self):
        for widget in self.table_frame.winfo_children():
            widget.destroy()
        self.entries = []

        if self.data is not None:
            for idx, column in enumerate(self.data.columns):
                label = tk.Label(self.table_frame, text=column, bg='lightgrey', font=('Arial', 10, 'bold'))
                label.grid(row=0, column=idx, padx=5, pady=5)
            
            for i, row in self.data.iterrows():
                row_entries = []
                for j, value in enumerate(row):
                    if j < 2:  # First two columns as Entry widgets
                        entry = tk.Entry(self.table_frame, font=('Arial', 10))
                        entry.grid(row=i+1, column=j, padx=5, pady=5)
                        entry.insert(0, value)
                        row_entries.append(entry)
                    else:  # Columns from the third onwards as Buttons
                        button_frame = tk.Frame(self.table_frame)
                        button_frame.grid(row=i+1, column=j, padx=5, pady=5)
                        var = tk.StringVar(value=str(value))
                        true_button = tk.Radiobutton(button_frame, text='True', variable=var, value='True', indicatoron=0, command=lambda i=i, j=j, var=var: self.set_value(i, j, var.get()), bg='#28a745', fg='white', selectcolor='green', relief='raised', bd=5)
                        false_button = tk.Radiobutton(button_frame, text='False', variable=var, value='False', indicatoron=0, command=lambda i=i, j=j, var=var: self.set_value(i, j, var.get()), bg='#dc3545', fg='white', selectcolor='red', relief='raised', bd=5)
                        true_button.pack(side=tk.LEFT)
                        false_button.pack(side=tk.LEFT)
                        row_entries.append((true_button, false_button, var))
                self.entries.append(row_entries)

    def set_value(self, row, col, value):
        self.data.iat[row, col] = value == 'True'

    def adjust_window_size(self):
        self.root.update_idletasks()
        width = max(self.root.winfo_width(), 500)
        height = max(self.root.winfo_height(), 200)
        self.root.geometry(f"{width}x{height}")

    def save_changes(self):
        if self.data is not None and self.filepath is not None:
            for i, row_entries in enumerate(self.entries):
                for j, entry in enumerate(row_entries):
                    if j < 2:  # First two columns
                        value = entry.get()
                        self.data.iat[i, j] = value
                    else:  # From third column onwards
                        value = entry[2].get()
                        self.data.iat[i, j] = value == 'True'
            self.data.to_csv(self.filepath, index=False)
            messagebox.showinfo("Info", "Änderungen gespeichert")

    def set_all_false(self):
        if self.data is not None:
            for i, row_entries in enumerate(self.entries):
                for j, entry in enumerate(row_entries):
                    if j >= 2:  # Only from third column onwards
                        entry[1].select()  # Select 'False' button
                        self.data.iat[i, j] = False

root = tk.Tk()
app = CSVEditor(root)
root.mainloop()