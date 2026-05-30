import requests

from .documents_localization import normalize_language


AI_GENERATOR_URL = "https://etha-hypercatalectic-rueben.ngrok-free.dev/generate"


def send_to_generator(template_name, values, language="ru"):
    language = normalize_language(language)

    payload = {
        "template_name": template_name,
        "values": values,
        "language": language,
    }

    try:
        response = requests.post(
            AI_GENERATOR_URL,
            json=payload,
            timeout=120
        )
    except requests.RequestException as exc:
        return {
            "error": True,
            "status_code": None,
            "response": str(exc),
            "payload_sent": payload
        }

    try:
        response_data = response.json()
    except Exception:
        response_data = response.text

    if response.status_code >= 400:
        return {
            "error": True,
            "status_code": response.status_code,
            "response": response_data,
            "payload_sent": payload
        }

    return {
        "error": False,
        "status_code": response.status_code,
        "response": response_data
    }