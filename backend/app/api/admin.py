from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.database.postgres import get_db
from backend.app.models.document import Document
from backend.app.rag.pipeline import RAGPipeline
import os
import shutil

router = APIRouter()
rag_pipeline = RAGPipeline()
UPLOAD_DIR = "uploads"

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

@router.post("/upload")
async def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="non pdf files are not yet supported")

    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    
    db_doc = Document(filename=file.filename, status="processing")
    db.add(db_doc)
    db.commit()
    db.refresh(db_doc)

    # Process PDF and add to vector store with document_id
    success = await rag_pipeline.process_pdf(file_path, db_doc.id)
    
    if success:
        db_doc.status = "processed"
    else:
        db_doc.status = "error"
    
    db.commit()

    return {"filename": file.filename, "status": db_doc.status}

@router.get("/")
async def list_documents(db: Session = Depends(get_db)):
    return db.query(Document).all()

@router.delete("/delete/{document_id}")
async def delete_document(document_id: int, db: Session = Depends(get_db)):
    print(f"DEBUG: Deleting document with ID: {document_id}")
    db_doc = db.query(Document).filter(Document.id == document_id).first()
    if not db_doc:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # 1. Delete from Vectorstore
    rag_pipeline.delete_document(document_id)
    
    # 2. Delete physical file
    file_path = os.path.join(UPLOAD_DIR, db_doc.filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        
    # 3. Delete from DB
    db.delete(db_doc)
    db.commit()
    
    return {"message": "Document deleted successfully"}
