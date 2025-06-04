import tkinter as tk
from tkinter import messagebox
import sqlite3

class Layout:
    def __init__(self, root):
        self.root = root
        self.root.title("Zarządzanie Bazą Danych")

        # Lista kolumn
        self.columns = ["id", "nazwa", "opis", "kategoria"]
        self.entries = {}

        # Pola wejściowe
        for index, column in enumerate(self.columns):
            label = tk.Label(root, text=f"{column.capitalize()}:")
            label.grid(row=index, column=0)
            entry = tk.Entry(root)
            entry.grid(row=index, column=1)
            self.entries[column] = entry

        # Pole na ilość wierszy
        self.row_count_label = tk.Label(root, text="Ilość wierszy:")
        self.row_count_label.grid(row=len(self.columns), column=0)
        self.row_count_entry = tk.Entry(root)
        self.row_count_entry.grid(row=len(self.columns), column=1)

        # Przyciski
        tk.Button(root, text="Dodaj", command=self.insert).grid(row=len(self.columns)+1, column=0)
        tk.Button(root, text="Usuń", command=self.delete).grid(row=len(self.columns)+1, column=1)
        tk.Button(root, text="Szukaj", command=self.find).grid(row=len(self.columns)+2, column=0)
        tk.Button(root, text="Aktualizuj", command=self.update).grid(row=len(self.columns)+2, column=1)
        tk.Button(root, text="Pokaż ostatnie", command=self.show_last_rows).grid(row=len(self.columns)+3, column=0, columnspan=2)

        self.add_custom_widgets()

        # Tekstowe pole wyników
        self.output = tk.Text(root, height=10, width=50)
        self.output.grid(row=len(self.columns)+4, column=0, columnspan=2)

    def add_custom_widgets(self):
        pass

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS dane (
                id TEXT PRIMARY KEY,
                nazwa TEXT,
                opis TEXT,
                kategoria TEXT
            )
        """)
        self.conn.commit()

    def insert(self) -> None:
        pass

    def delete(self) -> None:
        pass

    def find(self) -> None:
        pass

    def update(self) -> None:
        pass

    def show_last_rows(self) -> None:
        pass

    def requirements(self, requirements: dict[str, str]) -> dict[str, str]:
        return requirements


if __name__ == "__main__":
    root = tk.Tk()
    app = Layout(root)
    root.mainloop()
