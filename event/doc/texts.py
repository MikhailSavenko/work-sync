from common.variables import (
    CONFLICT_DATA,
    FORBIDDEN_403_RUSSIAN,
    FORBIDDEN_DESCRIPTION,
    MEETING_WORKER_CONFLICT_DATETIME,
    NO_MEETING,
    NO_VALID_STRING,
    NOT_FOUND_DESCRIPTION,
    VALIDATION_ERROR_DESCRIPTION,
    WRONG_PARAM_DONE,
)

TAGS_MEETINGS = ["Meetings"]

MEETING_TEXTS = {
    "me": {
        "tags": TAGS_MEETINGS,
        "summary": "Получение встреч пользователя",
        "description": "Встречи в которых участвует сотрудник",
        "done_param": {
            "description": "Фильтр встреч по времени (0 - предстоящие, 1 - все, включая прошедшие)",
            "enum": ["0", "1"],
            "default": "0",
        },
        "responses": {"200": "Список встреч", "400": "Некорректный параметр done"},
        "example": {"400": {"detail": WRONG_PARAM_DONE}},
    },
    "list": {
        "tags": TAGS_MEETINGS,
        "summary": "Список всех встреч",
        "description": "Список всех встреч на площадке: и предстоящие и прошедшие",
        "responses": {"200": "Список встреч"},
    },
    "read": {
        "tags": TAGS_MEETINGS,
        "summary": "Получить встречу по ID",
        "description": "Детальная информация о конкретной встрече",
        "responses": {"200": "Встреча", "404": NOT_FOUND_DESCRIPTION},
        "example": {"404": {"detail": NO_MEETING}},
    },
    "create": {
        "tags": TAGS_MEETINGS,
        "summary": "Создание новой встречи",
        "description": "Позволяет создать новую встречу с указанными параметрами. Возвращает созданный объект встречи.",
        "responses": {"201": "Встреча создана", "400": VALIDATION_ERROR_DESCRIPTION, "409": CONFLICT_DATA},
        "example": {
            "400": {"description": [NO_VALID_STRING]},
            "409": {"detail": MEETING_WORKER_CONFLICT_DATETIME},
        },
    },
    "update": {
        "tags": TAGS_MEETINGS,
        "summary": "Изменение встречи",
        "description": "Позволяет изменить существующую встречу",
        "responses": {
            "400": VALIDATION_ERROR_DESCRIPTION,
            "403": FORBIDDEN_DESCRIPTION,
            "409": CONFLICT_DATA,
            "404": NOT_FOUND_DESCRIPTION,
        },
        "example": {
            "400": {"non_field_errors": ["Встреча должна включать минимум двух участников."]},
            "409": {"detail": MEETING_WORKER_CONFLICT_DATETIME},
            "403": {"detail": FORBIDDEN_403_RUSSIAN},
            "404": {"detail": NO_MEETING},
        },
    },
    "delete": {
        "tags": TAGS_MEETINGS,
        "summary": "Отмена встречи",
        "description": "Позволяет удалить существующую встречу",
        "responses": {"404": NOT_FOUND_DESCRIPTION, "403": FORBIDDEN_DESCRIPTION},
        "example": {"403": {"detail": FORBIDDEN_403_RUSSIAN}, "404": {"detail": NO_MEETING}},
    },
}
