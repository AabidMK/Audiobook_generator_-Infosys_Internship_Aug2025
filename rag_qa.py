from rag_query import answer_question

print("=== Testing Interactive RAG Query ===")
print("Type 'exit' to quit.\n")

while True:
    user_question = input("Enter your question: ").strip()
    if user_question.lower() in ["exit", "quit"]:
        print("Exiting RAG test.")
        break

    try:
        answer, citations = answer_question(user_question)
        print("\nANSWER:\n", answer)
        print("\nCITATIONS:")
        for c in citations:
            print(c)
    except Exception as e:
        print("Error during RAG query:", e)