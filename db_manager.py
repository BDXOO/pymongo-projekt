import pymongo as pyM
from pymongo.errors import ConnectionFailure, OperationFailure
from typing import List, Dict, Any, Optional

class db_API:
    def __init__(self, uri: str, db_name: str) -> None:
        """
        Args:
            uri (str): The MongoDB connection URI.
            db_name (str): The name of the database to use.
        """
        self.uri: str = uri
        self.db_name: str = db_name
        self.client: Optional[pyM.MongoClient] = None
        self.db: Optional[pyM.database.Database] = None
        
        print(f"db_API initialized for URI: {self.uri}, Database: {self.db_name}")
        self.main()

    def main(self) -> None:
        """
        Main setup method, called on initialization.
        Attempts to connect to the database.
        """
        print("Executing main setup...")
        if self.db_connect():
            print(f"Successfully connected to MongoDB and database '{self.db_name}' established in main().")
        else:
            raise "Failed to connect to MongoDB in main(). Please check URI and server status."

    def db_connect(self) -> bool:
        if self.client and self.db:
            print("Already connected to the database.")
            return True
        try:
            print(f"Attempting to connect to MongoDB at {self.uri}...")
            self.client = pyM.MongoClient(self.uri, serverSelectionTimeoutMS=5000)
            # Verify connection
            self.client.admin.command('ismaster') 
            self.db = self.client[self.db_name]
            print(f"Successfully connected to MongoDB and selected database: {self.db_name}")
            return True
        except ConnectionFailure as e:
            print(f"MongoDB connection failed: {e}")
            self.client = None
            self.db = None
            return False
        except Exception as e: # Catch other potential errors during connection setup
            print(f"An unexpected error occurred during connection: {e}")
            self.client = None
            self.db = None
            return False

    def db_disconnect(self) -> bool:
        """
        Returns:
            bool: True if disconnection was successful or if not connected, False on error.
        """
        if self.client:
            try:
                print("Disconnecting from MongoDB...")
                self.client.close()
                self.client = None
                self.db = None
                print("Successfully disconnected from MongoDB.")
                return True
            except Exception as e:
                print(f"Error during disconnection: {e}")
                return False
        else:
            print("Not connected, no need to disconnect.")
            return True # Considered successful as the state is "disconnected"

    def _get_collection(self, collection_name: str):
        """Helper method to get a collection object and check DB connection."""
        if self.db is None:
            print("Error: Not connected to any database. Call db_connect() first or ensure main() succeeded.")
            return None
        try:
            return self.db[collection_name]
        except Exception as e:
            print(f"Error accessing collection '{collection_name}': {e}")
            return None

    def insert(self, collection_name: str, document: Dict[str, Any] = None, documents: List[Dict[str, Any]] = None) -> bool:
        """
        `document`: single insert
        `documents`: bult insert
        Args:
            collection_name (str): The name of the collection.
            document (Dict[str, Any], optional): The document to insert.
            documents (List[Dict[str, Any]], optional): A list of documents to insert.
        Returns:
            bool: True if insert is successful, False otherwise
        """
        collection = self._get_collection(collection_name)
        if collection is None:
            return False

        try:
            if document and documents:
                # print("Error: Provide either 'document' for single insert or 'documents' for bulk, not both.")
                return False
            if document:
                result = collection.insert_one(document)
                print(f"Inserted 1 document into '{collection_name}'. ID: {result.inserted_id}")
                return True
            elif documents:
                result = collection.insert_many(documents)
                print(f"Inserted {len(result.inserted_ids)} documents into '{collection_name}'. IDs: {result.inserted_ids}")
                return True
            else:
                print("Error: No document(s) provided for insertion.")
                return False
        except OperationFailure as e:
            print(f"Error inserting document(s) into '{collection_name}': {e.details}")
            return False
        except Exception as e:
            print(f"An unexpected error occurred during insert: {e}")
            return False

    def delete(self, collection_name: str, query: Dict[str, Any], delete_many: bool = False) -> bool:
        """
        Args:
            collection_name (str): The name of the collection.
            query (Dict[str, Any]): The query to select documents for deletion.
            delete_many (bool): If True, deletes all matching documents. Otherwise, deletes one.
        Returns:
            bool: True if delete is successful, False otherwise
        """
        collection = self._get_collection(collection_name)
        if collection is None:
            return False

        try:
            if delete_many:
                result = collection.delete_many(query)
                print(f"Deleted {result.deleted_count} documents from '{collection_name}' matching query.")
                return True
            else:
                result = collection.delete_one(query)
                print(f"Deleted {result.deleted_count} document from '{collection_name}' matching query.")
                return True
        except OperationFailure as e:
            print(f"Error deleting document(s) from '{collection_name}': {e.details}")
            return False
        except Exception as e:
            print(f"An unexpected error occurred during delete: {e}")
            return False

    def find(self, collection_name: str, query: Dict[str, Any] = None, find_one: bool = False, projection: Optional[Dict[str, int]] = None):
        """
        Args:
            collection_name (str): The name of the collection.
            query (Dict[str, Any], optional): The query to filter documents. Defaults to {} (all documents).
            find_one (bool): If True, finds and prints a single document. Otherwise, finds all matching.
            projection (Optional[Dict[str, int]]): Specifies which fields to include or exclude.
        Returns:
            None: find error / collection is empty
            dict[str, str]: [collection_name: ]
        """
        collection = self._get_collection(collection_name)
        if collection is None:
            return

        if query is None:
            query = {} # Default to finding all if no query is specified

        try:
            if find_one:
                document = collection.find_one(query, projection=projection)
                if document:
                    return {collection_name: document}
                else:
                    return None
            else:
                cursor = collection.find(query, projection=projection)
                documents_found = list(cursor) # Consume cursor to check if any were found
                if documents_found:
                    return {collection_name: documents_found}
                else:
                    return None
        except Exception:
            return None

    def update(self, collection_name: str, query: Dict[str, Any], update_data: Dict[str, Any], update_many: bool = False, upsert: bool = False) -> bool:
        """
        Args:
            collection_name (str): The name of the collection.
            query (Dict[str, Any]): The query to select documents for update.
            update_data (Dict[str, Any]): The update operations (e.g., {'$set': {'key': 'value'}}).
            update_many (bool): If True, updates all matching documents. Otherwise, updates one.
            upsert (bool): If True, creates a new document if no document matches the query.
        Returns:
            bool: True if update is successful, False otherwise
        """
        collection = self._get_collection(collection_name)
        if collection is None:
            return False

        if not update_data:
            return False
            
        try:
            if update_many:
                result = collection.update_many(query, update_data, upsert=upsert)
            else:
                result = collection.update_one(query, update_data, upsert=upsert)
            
            # print(f"Matched {result.matched_count} document(s) in '{collection_name}'.")
            if result.upserted_id:
                # print(f"Upserted ID: {result.upserted_id}")
                return True
            else:
                return True
                # print(f"Modified {result.modified_count} document(s).")
        except Exception:
            return False