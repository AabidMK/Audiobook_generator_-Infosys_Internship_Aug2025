from ragutils import query_with_gemini,create_collection
query = "What is called neuron ?"
collection=create_collection()
answer, chunks = query_with_gemini(query, collection)
print("\nAnswer:\n", answer)
print("\nCitations:")
for i, c in enumerate(chunks):
    print(f"[{i+1}] {c['file_path']} - Chunk {c['chunk_index']} (Score: {c['distance']:.4f})")
