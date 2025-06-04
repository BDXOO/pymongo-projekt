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

    def add_custom_widgets(self):
        self.collection_var = tk.StringVar(value=self.collection)
        self.collection_menu = tk.OptionMenu(self.root, self.collection_var, self.collection, command=self.switch_collection)
        self.collection_menu.grid(row=len(self.columns)+5, column=0, columnspan=2)

        self.new_collection_entry = tk.Entry(self.root)
        self.new_collection_entry.grid(row=len(self.columns)+6, column=0)
        tk.Button(self.root, text="Nowa kolekcja", command=self.create_collection).grid(row=len(self.columns)+6, column=1)

        self.update_collection_menu()

    def switch_collection(self, name: str):
        self.collection = name
        self.output.insert(tk.END, f"Przełączono na kolekcję: {name}\n")

    def create_collection(self):
        new_name = self.new_collection_entry.get().strip()
        if not new_name:
            messagebox.showwarning("Błąd", "Wprowadź nazwę nowej kolekcji.")
            return
        created = self.api.insert(new_name, document={"__init__": True})
        if created:
            self.api.delete(new_name, {"__init__": True})
            self.update_collection_menu()
            self.collection_var.set(new_name)
            self.switch_collection(new_name)
        else:
            messagebox.showerror("Błąd", "Nie udało się utworzyć kolekcji.")

    def update_collection_menu(self):
        if self.api.db is None:
            return
        menu = self.collection_menu["menu"]
        menu.delete(0, "end")
        collections = self.api.db.list_collection_names()
        for name in collections:
            menu.add_command(label=name, command=lambda value=name: self.switch_collection(value))

    def insert(self) -> None:
        data = {column: self.entries[column].get() for column in self.columns}
        if not all(data.values()):
            self.output.insert(tk.END, "Wszystkie pola muszą być wypełnione.\n")
            return
        success = self.api.insert(self.collection, document=data)
        self.output.insert(tk.END, f"{'Dodano' if success else 'Błąd'}: {data}\n")

    def delete(self) -> None:
        id_value = self.entries["id"].get()
        if not id_value:
            messagebox.showwarning("Brak ID", "Wprowadź ID do usunięcia.")
            return
        confirm = messagebox.askyesno("Potwierdzenie", f"Czy na pewno usunąć ID={id_value}?")
        if confirm:
            success = self.api.delete(self.collection, query={"id": id_value})
            msg = f"Usunięto rekord ID={id_value}" if success else f"Błąd lub brak ID={id_value}"
            self.output.insert(tk.END, msg + "\n")

    def find(self) -> None:
        id_value = self.entries["id"].get()
        result = self.api.find(self.collection, query={"id": id_value}, find_one=True)
        self.output.insert(tk.END, f"{'Znaleziono' if result else 'Nie znaleziono'}: {result}\n")

    def update(self) -> None:
        data = {column: self.entries[column].get() for column in self.columns}
        if not data["id"]:
            self.output.insert(tk.END, "Musisz podać ID do aktualizacji.\n")
            return
        update_data = {k: v for k, v in data.items() if k != "id"}
        success = self.api.update(self.collection, query={"id": data["id"]}, update_data={"$set": update_data})
        msg = "Zaktualizowano" if success else "Nie udało się zaktualizować"
        self.output.insert(tk.END, f"{msg} dane: {data}\n")

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
