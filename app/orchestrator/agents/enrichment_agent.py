import json
from app.orchestrator.utils.llm import call_llm

def suggest_enrichment(question: str, missing_info: str):
    """
    Suggest enrichment actions based on missing information.
    Ensures the output is always valid JSON.
    """
    prompt = f"""
    You are an enrichment planner AI.

    User question: {question}
    Missing information: {missing_info}

    Respond ONLY with valid JSON array.
    Each item must have:
      - "type": one of ["upload", "connect", "fetch"]
      - "label": a short action description

    Example format:
    [
      {{ "type": "upload", "label": "Upload Q3 report" }},
      {{ "type": "connect", "label": "Connect SharePoint HR policies" }}
    ]

    Do not include explanations or markdown fences.
    """
    raw = call_llm(prompt).strip()

    try:
        if "```" in raw:
            raw = raw.split("```json")[-1].split("```")[0].strip()
        return json.loads(raw)
    except Exception as e:
        return [
            {
                "type": "manual_review",
                "label": f"JSON parse error: {str(e)}",
                "raw_output": raw[:200]
            }
        ]