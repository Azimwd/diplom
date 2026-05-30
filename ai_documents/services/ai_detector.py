import requests

from .documents import DOCUMENT_TYPES
from .documents_localization import (
    get_localized_documents,
    normalize_language,
)


AI_DOCUMENT_DETECT_URL = "https://etha-hypercatalectic-rueben.ngrok-free.dev/documents/match-template"


def detect_document_type(question: str, language: str = "ru"):
    language = normalize_language(language)

    documents = get_localized_documents(DOCUMENT_TYPES, language)

    payload = {
        "question": question,
        "language": language,
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
            "error": "AI returned non-json response",
            "status_code": response.status_code,
            "raw_response": response.text[:1000]
        }

    if response.status_code >= 400:
        return {
            "intent": "unknown",
            "found": False,
            "template_name": None,
            "confidence": 0,
            "error": "AI returned error",
            "status_code": response.status_code,
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

    if intent in ["documents_list", "clarification", "unknown"]:
        return {
            "intent": intent,
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