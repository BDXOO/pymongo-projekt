#from layout import Layout
#from db_manager import *
#
#
## --- Example Usage ---
#if __name__ == "__main__":
#    # Replace with your MongoDB URI and database name
#    # For local MongoDB without auth:
#    MONGO_URI = "mongodb://localhost:27017/"
#    # For MongoDB Atlas, get the URI from your cluster's connect dialog
#    # MONGO_URI = "mongodb+srv://<username>:<password>@<cluster-url>/?retryWrites=true&w=majority"
#    DB_NAME = "NoName"
#
#    print("--- Initializing db_API ---")
#    # The API connects automatically in __init__ via main()
#    api = db_API(uri=MONGO_URI, db_name=DB_NAME)
#
#    # Check if connection was successful (optional, as methods internally check self.db)
#    if api.db is not None:
#        print("\n--- Testing CRUD Operations ---")
#        COLLECTION_NAME = "mycollection"
#
#        # # Insert
#        # print(f"\n--- Inserting into '{COLLECTION_NAME}' ---")
#        # api.insert(COLLECTION_NAME, document={"name": "Ash", "role": "user", "age": 30})
#        # api.insert(COLLECTION_NAME, documents=[
#        #     {"name": "Jane", "role": "admin", "age": 28},
#        #     {"name": "Doe", "role": "user", "age": 45}
#        # ])
#
#        # # Find
#        # print(f"\n--- Finding in '{COLLECTION_NAME}' ---")
#        # print(api.find(COLLECTION_NAME, query={})) # Find all records
#        # print(api.find(COLLECTION_NAME, query={"role": "user"})) # Find all users
#        # print(api.find(COLLECTION_NAME, query={"name": "Jane"}, find_one=True)) # Find one specific user
#        # print(api.find(COLLECTION_NAME, query={"name": "NonExistent"}, find_one=True)) # Try to find non-existent user
#
#        # # Update
#        # print(f"\n--- Updating in '{COLLECTION_NAME}' ---")
#        # api.update(COLLECTION_NAME, query={"name": "Ash"}, update_data={"$set": {"age": 31, "status": "active"}})
#        # api.find(COLLECTION_NAME, query={"name": "Ash"}, find_one=True) # Verify update
#        
#        # # Update with upsert for a new user
#        # print(f"\n--- Updating with upsert in '{COLLECTION_NAME}' ---")
#        # api.update(COLLECTION_NAME, query={"name": "Kate"}, update_data={"$set": {"age": 25, "role": "editor"}}, upsert=True)
#        # api.find(COLLECTION_NAME, query={"name": "Kate"}, find_one=True) # Verify upsert
#
#        # # Delete
#        # print(f"\n--- Deleting from '{COLLECTION_NAME}' ---")
#        # api.delete(COLLECTION_NAME, query={"name": "Doe"}) # Delete one user
#        # api.find(COLLECTION_NAME, query={"name": "Doe"}, find_one=True) # Verify delete
#
#        # Clean up: Delete all users for next run (optional)
#        # print(f"\n--- Cleaning up '{COLLECTION_NAME}' ---")
#        # api.delete(COLLECTION_NAME, query={}, delete_many=True)
#        # api.find(COLLECTION_NAME)
#
#
#    print("\n--- Disconnecting ---")
#    api.db_disconnect()
#
#    print("\n--- Attempting operations after disconnect ---")
#    api.find(COLLECTION_NAME, query={"name": "Ash"}, find_one=True) # Should indicate not connected

import tkinter as tk
from tkinter import messagebox
from layout import Layout
from db_manager import db_API

class DBApp(Layout):
    def __init__(self, root, api, collection_name="mycollection"):
        self.api = api
        self.collection = collection_name
        super().__init__(root)

    def insert(self) -> None:
        data = {}
        for column in self.columns:
            value = self.entries[column].get()
            if not value:
                messagebox.showwarning("Błąd", f"Puste pole: {column}")
                return
            data[column] = value

        success = self.api.insert(self.collection, document=data)
        if success:
            self.output.insert(tk.END, f"Dodano: {data}\n")
        else:
            self.output.insert(tk.END, "Błąd podczas dodawania.\n")

    def delete(self) -> None:
        id_value = self.entries["id"].get()
        if not id_value:
            messagebox.showwarning("Błąd", "Musisz podać ID do usunięcia.")
            return

        confirm = messagebox.askyesno("Potwierdzenie", f"Czy na pewno usunąć ID={id_value}?")
        if confirm:
            success = self.api.delete(self.collection, query={"id": id_value})
            if success:
                self.output.insert(tk.END, f"Usunięto rekord ID={id_value}\n")
            else:
                self.output.insert(tk.END, "Nie udało się usunąć rekordu.\n")

    def find(self) -> None:
        id_value = self.entries["id"].get()
        result = self.api.find(self.collection, query={"id": id_value}, find_one=True) if id_value else self.api.find(self.collection)

        if result:
            self.output.insert(tk.END, f"Wyniki: {result}\n")
        else:
            self.output.insert(tk.END, "Brak wyników.\n")

    def update(self) -> None:
        id_value = self.entries["id"].get()
        if not id_value:
            messagebox.showwarning("Błąd", "Musisz podać ID do aktualizacji.")
            return

        update_data = {}
        for column in self.columns:
            if column == "id":
                continue
            value = self.entries[column].get()
            update_data[column] = value

        success = self.api.update(self.collection, query={"id": id_value}, update_data={"$set": update_data})
        if success:
            self.output.insert(tk.END, f"Zaktualizowano rekord ID={id_value}.\n")
        else:
            self.output.insert(tk.END, "Nie udało się zaktualizować rekordu.\n")

if __name__ == "__main__":
    MONGO_URI = "mongodb://localhost:27017/"
    DB_NAME = "NoName"
    COLLECTION_NAME = "mycollection"

    try:
        api = db_API(uri=MONGO_URI, db_name=DB_NAME)
    except Exception as e:
        print("Nie udało się połączyć z bazą danych.")
        exit(1)

    root = tk.Tk()
    app = DBApp(root, api, collection_name=COLLECTION_NAME)
    root.mainloop()

    api.db_disconnect()
