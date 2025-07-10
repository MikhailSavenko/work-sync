from rest_framework import status
from rest_framework.exceptions import APIException


class TeamConflictError(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_code = "team_conflict"
    default_detail = "Конфликт при создании команды!"


class ValidationDateError(APIException):
    default_detail = "Неверный формат даты."
    status_code = status.HTTP_400_BAD_REQUEST
