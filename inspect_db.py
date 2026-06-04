from backend.app.database.postgres import SessionLocal
from backend.app.models.document import Document

def inspect_db():
    db = SessionLocal()
    try:
        docs = db.query(Document).all()
        print("Documents in database:")
        for doc in docs:
            print(f"ID: {doc.id}, Filename: {doc.filename}, Status: {doc.status}")
    finally:
        db.close()

if __name__ == "__main__":
    inspect_db()
