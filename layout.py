import tkinter as tk
from tkinter import messagebox

class Layout:
    def __init__(self, root):
        self.root = root
        self.root.title("Zarządzanie Bazą Danych")

        # Lista kolumn jak w tabeli
        self.columns = ["id", "nazwa", "opis", "kategoria"]
        self.entries = {}  # Słownik: kolumna -> Entry

        # Tworzenie pól wejściowych
        for index, column in enumerate(self.columns):
            label = tk.Label(root, text=f"{column.capitalize()}:")
            label.grid(row=index, column=0)
            entry = tk.Entry(root)
            entry.grid(row=index, column=1)
            self.entries[column] = entry

        # Przyciski
        tk.Button(root, text="Dodaj", command=self.insert).grid(row=len(self.columns), column=0)
        tk.Button(root, text="Usuń", command=self.delete).grid(row=len(self.columns), column=1)
        tk.Button(root, text="Szukaj", command=self.find).grid(row=len(self.columns)+1, column=0)
        tk.Button(root, text="Aktualizuj", command=self.update).grid(row=len(self.columns)+1, column=1)

        # tekstowe na wyniki
        self.output = tk.Text(root, height=10, width=50)
        self.output.grid(row=len(self.columns)+2, column=0, columnspan=2)

    def insert(self) -> None:
        data = {}
        for column in self.columns:
            value = self.entries[column].get()
            data[column] = value
        # wstaw dane do bazy danych tutaj
        self.output.insert(tk.END, f"Dodano: {data}\n")

    def delete(self) -> None:
        id_value = self.entries["id"].get()
        confirm = messagebox.askyesno("Potwierdzenie", f"Czy na pewno usunąć ID={id_value}?")
        if confirm:
            # usuń rekord z bazy danych
            self.output.insert(tk.END, f"Usunięto rekord ID={id_value}\n")

    def find(self) -> None:
        id_value = self.entries["id"].get()
        # znajdź rekordy w bazie danych
        self.output.insert(tk.END, f"Wyszukano dane dla ID={id_value}: ...\n")

    def update(self) -> None:
        data = {}
        for column in self.columns:
            value = self.entries[column].get()
            data[column] = value
        # zaktualizuj dane w bazie
        self.output.insert(tk.END, f"Zaktualizowano dane: {data}\n")

    def requirements(self, requirements: dict[str, str]) -> dict[str, str]:
        # Tutaj możesz walidować pola (np. czy są wypełnione)
        return requirements

# Uruchomienie app
if __name__ == "__main__":
    root = tk.Tk()
    app = Layout(root)
    root.mainloop()