import requests


def ask_ai(question, telegram_id=None, source=None):
    response = requests.post(
        "https://your-ai-server/ask",
        json={
            "question": question,
            "telegram_id": telegram_id,
            "source": source
        },
        timeout=120
    )

    response.raise_for_status()

    return response.json()["answer"]