from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.exceptions import NotAuthenticated
import logging

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    # Сначала стандартный DRF handler
    response = drf_exception_handler(exc, context)

    if response is not None:
        message = response.data.get('detail', response.data)

        if isinstance(exc, (NotFound, ObjectDoesNotExist)):
            message = "Объявление не найдено"

        if isinstance(exc, ValidationError):
            message = "Ошибка валидации данных"
            return Response({
                "statusCode": response.status_code,
                "success": False,
                "data": None,
                "message": message,
                "errors": exc.detail
            }, status=response.status_code)
        
        if isinstance(exc, AuthenticationFailed):
            return Response({
                "statusCode": 401,
                "success": False,
                "data": None,
                "message": str(exc)
            }, status=status.HTTP_401_UNAUTHORIZED)
        if isinstance(exc, NotAuthenticated):
            return Response({
                "statusCode": 401,
                "success": False,
                "data": None,
                "message": str(exc)
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response({
            "statusCode": response.status_code,
            "success": False,
            "data": None,
            "message": message
        }, status=response.status_code)

    # Для всех необработанных исключений
    logger.exception(exc)
    return Response({
        "statusCode": 500,
        "success": False,
        "data": None,
        "message": "Внутренняя ошибка сервера"
    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
