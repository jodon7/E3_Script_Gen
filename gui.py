import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path

from main import generate_jsl


class JSLGui(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("FDC JSL Generator")
        self.geometry("600x250")

        self.csv_path = tk.StringVar()
        self.output_path = tk.StringVar(value="fdc_combined.jsl")

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Input CSV:").grid(row=0, column=0, sticky="w", padx=10, pady=10)
        tk.Entry(self, textvariable=self.csv_path, width=50).grid(row=0, column=1)
        tk.Button(self, text="Browse", command=self.browse_csv).grid(row=0, column=2)

        tk.Label(self, text="Output JSL:").grid(row=1, column=0, sticky="w", padx=10, pady=10)
        tk.Entry(self, textvariable=self.output_path, width=50).grid(row=1, column=1)
        tk.Button(self, text="Browse", command=self.browse_output).grid(row=1, column=2)

        tk.Button(
            self,
            text="Generate JSL",
            command=self.generate,
            bg="#4CAF50",
            fg="white",
            width=20
        ).grid(row=3, column=1, pady=30)

    def browse_csv(self):
        path = filedialog.askopenfilename(
            title="Select input CSV",
            filetypes=[("CSV Files", "*.csv")]
        )
        if path:
            self.csv_path.set(path)

    def browse_output(self):
        path = filedialog.asksaveasfilename(
            title="Save output JSL",
            defaultextension=".jsl",
            filetypes=[("JSL Files", "*.jsl")]
        )
        if path:
            self.output_path.set(path)

    def generate(self):
        if not self.csv_path.get():
            messagebox.showerror("Error", "Please select an input CSV file.")
            return

        try:
            generate_jsl(
                csv_file=Path(self.csv_path.get()),
                template_file=Path("fdc_template.txt"),
                output_file=Path(self.output_path.get())
            )
            messagebox.showinfo("Success", "JSL file created successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    app = JSLGui()
    app.mainloop()