from app.orchestrator.utils.llm import call_llm

def generate_answer(question: str, context: str):
    prompt = f"""
    You are a business assistant. Use ONLY the given context to answer.

    Context:
    {context}

    Question:
    {question}

    If context doesn't contain enough info, say what is missing.
    """
    answer = call_llm(prompt)
    return answer