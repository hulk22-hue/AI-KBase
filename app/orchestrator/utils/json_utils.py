import json
import re

def extract_json_from_text(text: str):
    """
    Try to pull the first JSON object or array from a messy LLM response.
    Returns (parsed_json, error_msg)
    """
    text = text.strip()

    try:
        return json.loads(text), None
    except Exception:
        pass

    if "```" in text:
        parts = re.split(r"```(?:json)?", text)
        for part in parts:
            part = part.strip("` \n")
            try:
                return json.loads(part), None
            except Exception:
                continue

    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        candidate = match.group(0)
        try:
            return json.loads(candidate), None
        except Exception as e:
            return None, f"found JSON-like block but couldn't parse: {e}"

    return None, "no JSON object found in text"