import chromadb
import os

CHROMA_PATH = "chroma_db"

def nuke_chroma_contents():
    if not os.path.exists(CHROMA_PATH):
        print(f"Directory {CHROMA_PATH} does not exist. Nothing to clear.")
        return

    try:
        client = chromadb.PersistentClient(path=CHROMA_PATH)
        collections = client.list_collections()
        
        if not collections:
            print("No collections found in ChromaDB.")
            return

        for col in collections:
            name = col.name if hasattr(col, 'name') else col
            print(f"Processing collection: {name}")
            
            collection = client.get_collection(name)
            results = collection.get()
            ids = results.get("ids", [])
            
            if ids:
                print(f"Deleting {len(ids)} documents from {name}...")
                collection.delete(ids=ids)
                print("Successfully cleared documents.")
            else:
                print(f"Collection {name} is already empty.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    nuke_chroma_contents()
