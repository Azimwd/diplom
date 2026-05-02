from rest_framework.renderers import JSONRenderer

class APIRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = renderer_context.get("response")
        if response is None:
            return super().render(data, accepted_media_type, renderer_context)

        success = 200 <= response.status_code < 300

        # Если data — dict и есть message, вытаскиваем его
        message = ""
        if isinstance(data, dict) and "message" in data:
            message = data.pop("message")  # убираем из data, чтобы не дублировать

        formatted = {
            "statusCode": response.status_code,
            "success": success,
            "data": data if success else None,
            "message": message
        }

        return super().render(formatted, accepted_media_type, renderer_context)
