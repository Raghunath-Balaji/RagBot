from backend.app.database.vectorstore import get_vectorstore
from collections import Counter

def inspect_chroma():
    vectorstore = get_vectorstore()
    collection = vectorstore._collection
    
    results = collection.get()
    
    print(f"Total documents in Chroma: {len(results['ids'])}")
    
    doc_ids = []
    for m in results['metadatas']:
        doc_ids.append(m.get('document_id', 'MISSING'))
        
    counts = Counter(doc_ids)
    print("Document ID counts:")
    for doc_id, count in counts.items():
        print(f"  {doc_id}: {count} (Type: {type(doc_id)})")

if __name__ == "__main__":
    inspect_chroma()
