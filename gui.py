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

        self.load_button = tk.Button(root, text="CSV Laden", command=self.load_csv, bg='blue', fg='white')
        self.load_button.pack(pady=10)

        self.table_frame = tk.Frame(root)
        self.table_frame.pack()

        self.save_button = tk.Button(root, text="Änderungen speichern", command=self.save_changes, bg='green', fg='white')
        self.save_button.pack(pady=10)

    def load_csv(self):
        self.filepath = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if self.filepath:
            self.data = pd.read_csv(self.filepath)
            self.show_table()

    def show_table(self):
        for widget in self.table_frame.winfo_children():
            widget.destroy()
        self.entries = []

        if self.data is not None:
            for idx, column in enumerate(self.data.columns):
                label = tk.Label(self.table_frame, text=column, bg='lightgrey')
                label.grid(row=0, column=idx)
            
            for i, row in self.data.iterrows():
                row_entries = []
                for j, value in enumerate(row):
                    entry = tk.Entry(self.table_frame)
                    entry.grid(row=i+1, column=j)
                    entry.insert(0, value)
                    row_entries.append(entry)
                self.entries.append(row_entries)

    def save_changes(self):
        if self.data is not None and self.filepath is not None:
            for i, row_entries in enumerate(self.entries):
                for j, entry in enumerate(row_entries):
                    self.data.iat[i, j] = entry.get()
            self.data.to_csv(self.filepath, index=False)
            messagebox.showinfo("Info", "Änderungen gespeichert")

root = tk.Tk()
app = CSVEditor(root)
root.mainloop()