from jwt import decode as jwt_decode
from django.conf import settings

def decode_token_unsafe(token):
    try:
        payload = jwt_decode(
            token,
            settings.SECRET_KEY,
            algorithms=["HS256"],
            options={"verify_exp": False}
        )
        return payload
    except Exception:
        return None
