import logging
from src.document_parser import DocumentParser
from src.text_chunker import TextChunker
from src.vector_store import VectorStore
from src.ollama_llm import LMStudioClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class QASystem:
    def __init__(self):
        self.vector_store = VectorStore()
        self.llm = LMStudioClient()

    def setup_rag(self, docs_dir="./documents"):
        """Ingests documents into the vector store."""
        parser = DocumentParser()
        chunker = TextChunker()
        docs = parser.read_text_files(docs_dir)
        if not docs:
            logger.warning("No documents found in ./documents directory.")
            return
        chunks = chunker.process_documents(docs)
        self.vector_store.add_chunks(chunks)
        logger.info("✅ RAG setup complete. System is ready.")

    def answer_question(self, question: str, n_results=3):
        """Answers a question using the RAG pipeline."""
        results = self.vector_store.query(question, n_results=n_results)
        
        context = ""
        citations = []
        
        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]

        for i, doc_text in enumerate(documents):
            context += doc_text + "\n\n"
            meta = metadatas[i]
            citations.append({
                "file_path": meta["source_file"],
                "chunk_index": meta["chunk_index"],
                "distance": distances[i]
            })

        if not context:
            return "Could not find any relevant information.", []

        answer = self.llm.generate(context, question)
        return answer, citations

def main():
    qa = QASystem()
    qa.setup_rag()
    
    question = input("Enter your question: ")
    answer, citations = qa.answer_question(question)
    
    print("---" * 20)
    print(f"❓ Question: {question}")
    print(f"✅ Answer: {answer}")
    print("\n📚 Citations:")
    for i, citation in enumerate(citations):
        print(f"  [{i+1}] {citation['file_path']} (Chunk: {citation['chunk_index']}, Distance: {citation['distance']:.4f})")
    print("---" * 20)

if __name__ == "__main__":
    main()
