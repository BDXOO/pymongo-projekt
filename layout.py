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

        # Tekstowe pole wyników
        self.output = tk.Text(root, height=10, width=50)
        self.output.grid(row=len(self.columns)+4, column=0, columnspan=2)

        # Połączenie z bazą danych
        self.conn = sqlite3.connect("baza.db")
        self.cursor = self.conn.cursor()
        self.create_table()

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
        data = {}
        for column in self.columns:
            data[column] = self.entries[column].get()

        try:
            self.cursor.execute("""
                INSERT INTO dane (id, nazwa, opis, kategoria)
                VALUES (?, ?, ?, ?)
            """, (data["id"], data["nazwa"], data["opis"], data["kategoria"]))
            self.conn.commit()
            self.output.insert(tk.END, f"Dodano: {data}\n")
        except sqlite3.IntegrityError:
            self.output.insert(tk.END, f"Błąd: ID={data['id']} już istnieje!\n")

    def delete(self) -> None:
        id_value = self.entries["id"].get()
        if not id_value:
            messagebox.showwarning("Brak ID", "Wprowadź ID do usunięcia.")
            return

        confirm = messagebox.askyesno("Potwierdzenie", f"Czy na pewno usunąć ID={id_value}?")
        if confirm:
            self.cursor.execute("DELETE FROM dane WHERE id = ?", (id_value,))
            self.conn.commit()
            if self.cursor.rowcount > 0:
                self.output.insert(tk.END, f"Usunięto rekord ID={id_value}\n")
            else:
                self.output.insert(tk.END, f"Brak rekordu o ID={id_value}\n")

    def find(self) -> None:
        id_value = self.entries["id"].get()
        self.cursor.execute("SELECT * FROM dane WHERE id = ?", (id_value,))
        result = self.cursor.fetchone()
        if result:
            self.output.insert(tk.END, f"Znaleziono: {result}\n")
        else:
            self.output.insert(tk.END, f"Nie znaleziono rekordu o ID={id_value}\n")

    def update(self) -> None:
        data = {}
        for column in self.columns:
            data[column] = self.entries[column].get()

        self.cursor.execute("""
            UPDATE dane SET nazwa = ?, opis = ?, kategoria = ?
            WHERE id = ?
        """, (data["nazwa"], data["opis"], data["kategoria"], data["id"]))
        self.conn.commit()

        if self.cursor.rowcount > 0:
            self.output.insert(tk.END, f"Zaktualizowano dane: {data}\n")
        else:
            self.output.insert(tk.END, f"Brak rekordu o ID={data['id']} do aktualizacji\n")

    def show_last_rows(self) -> None:
        count_text = self.row_count_entry.get()
        if not count_text.isdigit():
            self.output.insert(tk.END, "Błąd: Wpisz poprawną liczbę wierszy.\n")
            return
        count = int(count_text)

        self.cursor.execute("SELECT * FROM dane ORDER BY ROWID DESC LIMIT ?", (count,))
        results = self.cursor.fetchall()

        self.output.insert(tk.END, f"Ostatnie {count} rekordów:\n")
        for row in results:
            self.output.insert(tk.END, f"{row}\n")

    def requirements(self, requirements: dict[str, str]) -> dict[str, str]:
        return requirements


# Uruchomienie aplikacji
if __name__ == "__main__":
    root = tk.Tk()
    app = Layout(root)
    root.mainloop()