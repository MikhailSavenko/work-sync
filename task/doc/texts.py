from common.variables import DEADLINE_NOT_WILL_BE_PAST, EVALUATION_CREATE_CONFLICT, NO_VALID_STRING, REQUIRED_FIELD, NO_TASK_COMM_TEXT, NO_TASK_EVAL_TEXT, NO_TASK, FORBIDDEN_403_RUSSIAN, CONFLICT_DATA, FORBIDDEN_403_DESCRIPTION, NOT_FOUND_DESCRIPTION, TASK_UPDATE_CONFLICT, VALIDATION_ERROR_DESCRIPTION, VALUE_LE_FIVE, WRONG_FORMAT_MUST_BE_INT

TAGS_TASKS = ["Tasks"]
TAGS_COMMENTS = ["Comments"]
TAGS_EVALUATIONS = ["Evaluations"]

TASK_TEXTS = {
    "me": {
        "tags": TAGS_TASKS,
        "summary": "Просмотр своих задач",
        "description": "Поздволяет посмотреть задачи текущего сотрудника",
        "responses": {"200": "", "400": ""},
        "example": {"400": {"error": ""}},
    },
    "list": {
        "tags": TAGS_TASKS,
        "summary": "Список всех задач",
        "description": "Список всех задач",
        "responses": {"200": ""},
    },
    "read": {
        "tags": TAGS_TASKS,
        "summary": "Просмотр определенной задачи",
        "description": "Показывает одну задачу",
        "responses": {"200": "", "404": NOT_FOUND_DESCRIPTION},
        "example": {"404": {"detail": NO_TASK}},
    },
    "create": {
        "tags": TAGS_TASKS,
        "summary": "Создание задачи",
        "description": "Позволяет создать новую задачу.",
        "responses": {"403": FORBIDDEN_403_DESCRIPTION, "400": VALIDATION_ERROR_DESCRIPTION},
        "example": {"400": {"deadline": [DEADLINE_NOT_WILL_BE_PAST]}, "403": {"detail": FORBIDDEN_403_RUSSIAN}},
    },
    "update": {
        "tags": TAGS_TASKS,
        "summary": "Обновление задачи",
        "description": "Позволяет обновить задачу полностью",
        "responses": {"403": FORBIDDEN_403_DESCRIPTION, "400": VALIDATION_ERROR_DESCRIPTION, "409": CONFLICT_DATA},
        "example": {
            "400": {"deadline": [DEADLINE_NOT_WILL_BE_PAST]},
            "409": {
                "task_update_conflict": {
                    "task_update_conflict": TASK_UPDATE_CONFLICT
                },
            },
            "403": {"detail": FORBIDDEN_403_RUSSIAN},
        },
    },
    "partial_update": {
        "tags": TAGS_TASKS,
        "summary": "Обновление отдельных полей задачи",
        "description": "Позволяет обновить одно поле у задачи",
        "responses": {"403": FORBIDDEN_403_DESCRIPTION, "400": VALIDATION_ERROR_DESCRIPTION, "409": CONFLICT_DATA},
        "example": {
            "400": {"deadline": [DEADLINE_NOT_WILL_BE_PAST]},
            "409": {
                "task_update_conflict": {
                    "task_update_conflict": TASK_UPDATE_CONFLICT
                },
            },
            "403": {"detail": FORBIDDEN_403_RUSSIAN},
        },
    },
    "delete": {
        "tags": TAGS_TASKS,
        "summary": "Удалить задачу",
        "description": "Позволяет удалить задачу",
        "responses": {"204": "", "403": FORBIDDEN_403_DESCRIPTION, "404": NOT_FOUND_DESCRIPTION},
        "example": {"403": {"detail": FORBIDDEN_403_RUSSIAN}, "404": {"detail": NO_TASK}},
    },
}


COMMENT_TEXTS = {
    "list": {
        "tags": TAGS_COMMENTS,
        "summary": "Список комментариев к задаче",
        "description": "Получить все комментарии для определенной задачи",
        "responses": {"400": VALIDATION_ERROR_DESCRIPTION, "404": NOT_FOUND_DESCRIPTION},
        "example": {"404": {"detail": NO_TASK}, "400": {"detail": WRONG_FORMAT_MUST_BE_INT}},
    },
    "create": {
        "tags": TAGS_COMMENTS,
        "summary": "Создать комментарий",
        "description": "Добавить новый комментарий к задаче",
        "responses": {"403": FORBIDDEN_403_DESCRIPTION, "400": VALIDATION_ERROR_DESCRIPTION, "404": NOT_FOUND_DESCRIPTION},
        "example": {
            "400": {"text": [REQUIRED_FIELD]},
            "404": {"detail": NO_TASK},
            "403": {"detail": FORBIDDEN_403_RUSSIAN},
        },
    },
    "read": {
        "tags": TAGS_COMMENTS,
        "summary": "Получить комментарий",
        "description": "Получить конкретный комментарий по ID",
        "responses": {"200": "", "400": VALIDATION_ERROR_DESCRIPTION, "404": NOT_FOUND_DESCRIPTION},
        "example": {
            "404": {"detail": NO_TASK_COMM_TEXT},
            "400": {"detail": WRONG_FORMAT_MUST_BE_INT},
        },
    },
    "partial_update": {
        "tags": TAGS_COMMENTS,
        "summary": "Обновить комментарий",
        "description": "Частично обновить комментарий",
        "responses": {
            "200": "",
            "400": VALIDATION_ERROR_DESCRIPTION,
            "403": FORBIDDEN_403_DESCRIPTION,
            "404": NOT_FOUND_DESCRIPTION,
        },
        "example": {
            "400": {"text": [NO_VALID_STRING]},
            "403": {"detail": FORBIDDEN_403_RUSSIAN},
            "404": {"detail": NO_TASK_COMM_TEXT},
        },
    },
    "delete": {
        "tags": TAGS_COMMENTS,
        "summary": "Удалить комментарий",
        "description": "Удалить комментарий",
        "responses": {"204": "", "403": FORBIDDEN_403_DESCRIPTION, "404": NOT_FOUND_DESCRIPTION},
        "example": {"403": {"detail": FORBIDDEN_403_RUSSIAN}, "404": {"detail": NO_TASK_COMM_TEXT}},
    },
}


EVALUATION_TEXTS = {
    "create": {
        "tags": TAGS_EVALUATIONS,
        "summary": "Создать оценку",
        "description": "Добавить новую оценку для задачи",
        "responses": {
            "403": FORBIDDEN_403_DESCRIPTION,
            "400": VALIDATION_ERROR_DESCRIPTION,
            "409": CONFLICT_DATA,
            "404": NOT_FOUND_DESCRIPTION,
        },
        "example": {
            "400": {"score": [VALUE_LE_FIVE]},
            "409": {"evaluation_create_conflict": EVALUATION_CREATE_CONFLICT},
            "403": {"detail": FORBIDDEN_403_RUSSIAN},
            "404": {"detail": NO_TASK},
        },
    },
    "partial_update": {
        "tags": TAGS_EVALUATIONS,
        "summary": "Частично обновить оценку",
        "description": "Обновить отдельные поля оценки",
        "responses": {
            "200": "",
            "400": VALIDATION_ERROR_DESCRIPTION,
            "403": FORBIDDEN_403_DESCRIPTION,
            "404": NOT_FOUND_DESCRIPTION,
        },
        "example": {
            "400": {"score": [VALUE_LE_FIVE]},
            "403": {"detail": FORBIDDEN_403_RUSSIAN},
            "404": {"detail": NO_TASK_EVAL_TEXT},
        },
    },
    "delete": {
        "tags": TAGS_EVALUATIONS,
        "summary": "Удалить оценку",
        "description": "Удалить оценку задачи",
        "responses": {"204": "", "403": FORBIDDEN_403_DESCRIPTION, "404": NOT_FOUND_DESCRIPTION},
        "example": {"403": {"detail": FORBIDDEN_403_RUSSIAN}, "404": {"detail": NO_TASK_EVAL_TEXT}},
    },
}
