from app.orchestrator.utils.llm import call_llm

def suggest_enrichment(question: str, missing_info: str):
    prompt = f"""
    You are an enrichment planner AI.

    User question: {question}
    Missing information: {missing_info}

    Based on the missing info, suggest 2-3 enrichment actions in JSON.
    - Use type "upload" if the user needs to provide internal files.
    - Use type "connect" if a system integration (like SharePoint, Confluence, API) is needed.
    - Use type "fetch" if the data can be fetched externally.

    Respond ONLY with JSON, e.g.:
    [
      {{ "type": "upload", "label": "Upload detailed report" }},
      {{ "type": "connect", "label": "Connect SharePoint policies" }}
    ]
    """
    response = call_llm(prompt)
    return response