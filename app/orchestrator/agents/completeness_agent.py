import json
from app.orchestrator.utils.llm import call_llm
from app.orchestrator.utils.json_utils import extract_json_from_text

def check_completeness(question: str, answer: str, context: str):
    prompt = f"""
    You are a strict JSON generator that evaluates answer completeness.

    Task:
    Evaluate whether the following answer completely addresses the question,
    based ONLY on the given context.

    Return ONLY valid JSON of this exact form:
    {{
      "completeness": "HIGH" | "MEDIUM" | "LOW",
      "missing_info": ["..."]
    }}

    Do NOT explain. Do NOT add any text after JSON.
    
    Question: {question}
    Answer: {answer}
    Context: {context}
    """
    response = call_llm(prompt).strip()
    parsed, err = extract_json_from_text(response)

    # try:
    #     if "```" in response:
    #         response = response.split("```json")[-1].split("```")[0].strip()
    #     return json.loads(response)
    # except Exception as e:
    #     return {"completeness": "UNKNOWN", "missing_info": [f"JSON parse error: {str(e)}", f"Raw: {response}"]}
    
    if parsed:
        # make sure keys exist
        return {
            "completeness": parsed.get("completeness", "UNKNOWN"),
            "missing_info": parsed.get("missing_info", []),
            "raw_llm": response
        }
    else:
        return {
            "completeness": "UNKNOWN",
            "missing_info": [
                f"JSON parse error: {err}",
                f"Raw: {response[:500]}"
            ],
        }