from ragutils import split_into_sentences,semantic_chunk,store_chunks,create_collection
def rag_call(text,file):
    collection = create_collection()
    sentences = split_into_sentences(text)
    chunks = semantic_chunk(sentences, threshold=0.75, overlap_sentences=1)
    store_chunks(collection, chunks,file)