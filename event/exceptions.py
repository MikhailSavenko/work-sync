from rest_framework.exceptions import APIException
from rest_framework import status


class MeetingConflictError(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_code = "meeting_conflict"
    default_detail = "Конфликт при создании встречи"