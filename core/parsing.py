import json

def parse_json_response(raw: str) -> dict | None:
    """
    Versucht die rohe Modellantwort als JSON zu parsen.
    Entfernt ggf. Markdown-Codeblöcke (```json ... ```).
    """
    clean = raw.strip()
    if clean.startswith("```"):
        clean = clean.split("\n", 1)[1]
        clean = clean.rsplit("```", 1)[0]
        clean = clean.strip()
    try:
        return json.loads(clean)
    except json.JSONDecodeError:
        return None
