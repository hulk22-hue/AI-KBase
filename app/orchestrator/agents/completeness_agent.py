from app.orchestrator.utils.llm import call_llm

def check_completeness(question: str, answer: str, context: str):
    prompt = f"""
    Evaluate if this answer completely addresses the question based on context.

    Question: {question}
    Answer: {answer}
    Context: {context}

    Return JSON with:
    {{
      "completeness": "HIGH" | "MEDIUM" | "LOW",
      "missing_info": ["..."] 
    }}
    """
    raw = call_llm(prompt)
    return raw