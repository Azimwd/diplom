
import requests
from django.conf import settings


def ask_ai_from_telegram(question, telegram_id=None, session_id=None):
    response = requests.post(
        "https://etha-hypercatalectic-rueben.ngrok-free.dev/ask",
        json={
            "question": question,
            "telegram_id": telegram_id,
            "session_id": session_id,
            "source": "telegram"
        },
        timeout=120
    )

    response.raise_for_status()
    data = response.json()

    return data.get("answer", "ИИ не вернул ответ.")