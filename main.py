import tkinter as tk
from tkinter import messagebox
from layout import Layout
from db_manager import db_API

class DBApp(Layout):
    def __init__(self, root, api, collection_name="mycollection"):
        self.api = api
        self.collection = collection_name

        self.conn = None
        self.cursor = None

        super().__init__(root)

    def insert(self) -> None:
        data = {column: self.entries[column].get() for column in self.columns}
        if not all(data.values()):
            self.output.insert(tk.END, "Wszystkie pola muszą być wypełnione.\n")
            return

        success = self.api.insert(self.collection, document=data)
        if success:
            self.output.insert(tk.END, f"Dodano: {data}\n")
        else:
            self.output.insert(tk.END, f"Błąd podczas dodawania danych.\n")

    def delete(self) -> None:
        id_value = self.entries["id"].get()
        if not id_value:
            messagebox.showwarning("Brak ID", "Wprowadź ID do usunięcia.")
            return

        confirm = messagebox.askyesno("Potwierdzenie", f"Czy na pewno usunąć ID={id_value}?")
        if confirm:
            success = self.api.delete(self.collection, query={"id": id_value})
            if success:
                self.output.insert(tk.END, f"Usunięto rekord ID={id_value}\n")
            else:
                self.output.insert(tk.END, f"Brak rekordu o ID={id_value} lub błąd podczas usuwania.\n")

    def find(self) -> None:
        id_value = self.entries["id"].get()
        result = self.api.find(self.collection, query={"id": id_value}, find_one=True)
        if result:
            self.output.insert(tk.END, f"Znaleziono: {result}\n")
        else:
            self.output.insert(tk.END, f"Nie znaleziono rekordu o ID={id_value}\n")

    def update(self) -> None:
        data = {column: self.entries[column].get() for column in self.columns}
        if not data["id"]:
            self.output.insert(tk.END, "Musisz podać ID do aktualizacji.\n")
            return

        update_data = {k: v for k, v in data.items() if k != "id"}
        success = self.api.update(self.collection, query={"id": data["id"]}, update_data={"$set": update_data})
        if success:
            self.output.insert(tk.END, f"Zaktualizowano dane: {data}\n")
        else:
            self.output.insert(tk.END, f"Nie udało się zaktualizować rekordu o ID={data['id']}\n")

    def show_last_rows(self) -> None:
        count_text = self.row_count_entry.get()
        if not count_text.isdigit():
            self.output.insert(tk.END, "Błąd: Wpisz poprawną liczbę wierszy.\n")
            return
        limit = int(count_text)

        result = self.api.find(self.collection)
        if not result or self.collection not in result:
            self.output.insert(tk.END, "Brak wyników w kolekcji.\n")
            return

        docs = result[self.collection][-limit:]
        self.output.insert(tk.END, f"Ostatnie {limit} rekordów:\n")
        for doc in docs:
            self.output.insert(tk.END, f"{doc}\n")


if __name__ == "__main__":
    MONGO_URI = "mongodb://localhost:27017/"
    DB_NAME = "NoName"
    COLLECTION_NAME = "mycollection"

    try:
        api = db_API(uri=MONGO_URI, db_name=DB_NAME)
    except Exception as e:
        print("Nie udało się połączyć z bazą danych MongoDB.")
        exit(1)

    root = tk.Tk()
    app = DBApp(root, api, collection_name=COLLECTION_NAME)
    root.mainloop()

    api.db_disconnect()
