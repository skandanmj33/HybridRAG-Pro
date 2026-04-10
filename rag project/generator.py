import ollama
from retriver import hybrid_search

def generate_answer(query):
    docs = hybrid_search(query)

    context = ""
    for i, doc in enumerate(docs):
        context += f"[Doc {i+1}]: {doc.page_content}\n\n"

    prompt = f"""
    You are an AI assistant.

    Answer the question clearly and concisely using ONLY the context below.

    DO NOT repeat the context.
    DO NOT say "the context says".
    Give a proper answer.

    Include citations like [Doc 1], [Doc 2] at the end of sentences.

    Context:
    {context}

    Question:
    {query}

    Answer:
    """

    response = ollama.chat(
        model="tinyllama",
        messages=[{"role": "user", "content": prompt}]
    )

    return response['message']['content']


if __name__ == "__main__":
    query = "What is cloud computing?"
    answer = generate_answer(query)
    print("\nFinal Answer:\n")
    print(answer)