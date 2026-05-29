import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from backend.app.database.vectorstore import get_vectorstore
import shutil
from langchain_cohere import CohereRerank
from langchain_classic.retrievers.contextual_compression import ContextualCompressionRetriever


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
        try:
            # 1. Initialize the Cohere Reranker
            compressor = CohereRerank(
                cohere_api_key=os.getenv("COHERE_API_KEY"), 
                model="rerank-english-v3.0", 
                top_n=k
            )
            
            # 2. Create a "Compression Retriever"
            # It will fetch 20 documents first, then Cohere will rerank them down to 'k'
            compression_retriever = ContextualCompressionRetriever(
                base_compressor=compressor, 
                base_retriever=self.vectorstore.as_retriever(search_kwargs={"k": 20})
            )
            
            # 3. Get the high-precision results
            results = compression_retriever.invoke(query)
            
            context = "\n\n".join([doc.page_content for doc in results])
            return context
        except Exception as e:
            print(f"Reranking failed or key missing, falling back to standard search: {e}")
            # Fallback to standard similarity search if Cohere fails (e.g., API key missing)
            results = self.vectorstore.similarity_search(query, k=k)
            return "\n\n".join([doc.page_content for doc in results])
