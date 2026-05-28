import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from backend.app.database.vectorstore import get_vectorstore
import shutil

class RAGPipeline:
    def __init__(self):
        self.vectorstore = get_vectorstore()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

    async def process_pdf(self, file_path: str, document_id: int):
        try:
            # 1. Load PDF
            loader = PyPDFLoader(file_path)
            docs = loader.load()

            # 2. Split text
            chunks = self.text_splitter.split_documents(docs)

            # Add document_id to metadata for precise deletion
            for chunk in chunks:
                chunk.metadata["document_id"] = document_id

            # 3. Add to Vectorstore
            self.vectorstore.add_documents(chunks)
            
            return True
        except Exception as e:
            print(f"Error processing PDF: {e}")
            return False

    def delete_document(self, document_id: int):
        try:
            self.vectorstore._collection.delete(where={"document_id": document_id})
            return True
        except Exception as e:
            print(f"Error deleting document from vectorstore: {e}")
            return False

    def get_relevant_context(self, query: str, k: int = 3):
        results = self.vectorstore.similarity_search(query, k=k)
        context = "\n\n".join([doc.page_content for doc in results])
        return context
