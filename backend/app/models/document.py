from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from backend.app.database.postgres import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    upload_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="pending") # pending or processed or error
