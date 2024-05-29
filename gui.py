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

        self.load_button = tk.Button(root, text="CSV Laden", command=self.load_csv, bg='#007bff', fg='white', font=('Arial', 12, 'bold'))
        self.load_button.pack(pady=20)

        self.table_frame = tk.Frame(root)
        self.table_frame.pack(pady=20)

        self.save_button = tk.Button(root, text="Änderungen speichern", command=self.save_changes, bg='#28a745', fg='white', font=('Arial', 12, 'bold'))
        self.save_button.pack(pady=20)

    def load_csv(self):
        self.filepath = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if self.filepath:
            self.data = pd.read_csv(self.filepath)
            self.show_table()
            self.adjust_window_size()

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
                    entry = tk.Entry(self.table_frame, font=('Arial', 10))
                    entry.grid(row=i+1, column=j, padx=5, pady=5)
                    entry.insert(0, value)
                    row_entries.append(entry)
                self.entries.append(row_entries)

    def adjust_window_size(self):
        self.root.update_idletasks()
        width = max(self.root.winfo_width(), 500)
        height = max(self.root.winfo_height(), 200)
        self.root.geometry(f"{width}x{height}")

    def save_changes(self):
        if self.data is not None and self.filepath is not None:
            for i, row_entries in enumerate(self.entries):
                for j, entry in enumerate(row_entries):
                    value = entry.get()
                    # Validierung nur ab der dritten Spalte (Index 2)
                    if j >= 2 and value not in ["True", "False"]:
                        messagebox.showerror("Fehler", f"Ungültiger Wert in Zeile {i+1}, Spalte {j+1}. Nur 'True' und 'False' sind erlaubt.")
                        return
                    self.data.iat[i, j] = value
            self.data.to_csv(self.filepath, index=False)
            messagebox.showinfo("Info", "Änderungen gespeichert")

root = tk.Tk()
app = CSVEditor(root)
root.mainloop()