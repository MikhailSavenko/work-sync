from rest_framework.exceptions import APIException
from rest_framework import status


class TaskConflictError(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_code = "task_conflict"
    default_detail = "Конфликт при обновлении задачи"



class EvaluationConflictError(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_code = "evaluation_conflict"
    default_detail = "Конфликт при создании оценки"