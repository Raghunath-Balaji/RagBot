from backend.app.database.postgres import SessionLocal
from backend.app.models.document import Document

db = SessionLocal()
docs = db.query(Document).all()
for doc in docs:
    print(f"ID: {doc.id}, Filename: {doc.filename}, Status: {doc.status}")
db.close()
