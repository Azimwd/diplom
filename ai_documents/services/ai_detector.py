import requests

from .documents import DOCUMENT_TYPES


AI_DOCUMENT_DETECT_URL = "https://etha-hypercatalectic-rueben.ngrok-free.dev/documents/match-template"


def detect_document_type(question: str):
    documents = [
        {
            "template_name": template_name,
            "title": data["title"]
        }
        for template_name, data in DOCUMENT_TYPES.items()
    ]

    payload = {
        "question": question,
        "documents": documents,
        "expected_response": {
            "intent": "documents_list | document_generation | clarification | unknown",
            "found": "boolean",
            "template_name": "string or null",
            "confidence": "number"
        }
    }

    try:
        response = requests.post(
            AI_DOCUMENT_DETECT_URL,
            json=payload,
            timeout=60
        )
    except requests.RequestException:
        return {
            "intent": "unknown",
            "found": False,
            "template_name": None,
            "confidence": 0,
            "error": "AI service unavailable"
        }

    try:
        result = response.json()
    except Exception:
        return {
            "intent": "unknown",
            "found": False,
            "template_name": None,
            "confidence": 0,
            "error": "AI returned non-json response"
        }

    if response.status_code >= 400:
        return {
            "intent": "unknown",
            "found": False,
            "template_name": None,
            "confidence": 0,
            "error": "AI returned error",
            "ai_response": result
        }

    intent = result.get("intent", "unknown")
    found = result.get("found", False)
    template_name = result.get("template_name")
    confidence = result.get("confidence", 0)

    allowed_intents = [
        "documents_list",
        "document_generation",
        "clarification",
        "unknown"
    ]

    if intent not in allowed_intents:
        intent = "unknown"

    if intent == "documents_list":
        return {
            "intent": "documents_list",
            "found": False,
            "template_name": None,
            "confidence": confidence
        }

    if intent == "clarification":
        return {
            "intent": "clarification",
            "found": False,
            "template_name": None,
            "confidence": confidence
        }

    if intent == "unknown":
        return {
            "intent": "unknown",
            "found": False,
            "template_name": None,
            "confidence": confidence
        }

    if intent == "document_generation":
        if not found:
            return {
                "intent": "clarification",
                "found": False,
                "template_name": None,
                "confidence": confidence
            }

        if template_name not in DOCUMENT_TYPES:
            return {
                "intent": "clarification",
                "found": False,
                "template_name": None,
                "confidence": 0,
                "error": "AI returned unknown template_name",
                "ai_template_name": template_name
            }

        return {
            "intent": "document_generation",
            "found": True,
            "template_name": template_name,
            "confidence": confidence
        }

    return {
        "intent": "unknown",
        "found": False,
        "template_name": None,
        "confidence": 0
    }