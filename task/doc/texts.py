VALIDATION_ERROR_DESCRIPTION = "Ошибки валидации"
CONFLICT_DATA = "Конфликт данных"
NOT_FOUND = "Объект не найден"

NO_TASK_COMM_TEXT = "No Task/Comment matches the given query."

TASK_TEXTS = {
    'me': {
        'summary': "Просмотр своих задач",
        'description': "Поздволяет посмотреть задачи текущего сотрудника",
        'responses': {
            '200': "",
            '400': ""
        },
        'example': {
            "400": {
                "error": ""
            }
        }
    },
    'list': {
        'summary': "Список всех задач",
        'description': "Список всех задач",
        'responses': {
            '200': ""
        }
    },
    'read': {
        'summary': "Просмотр определенной задачи",
        'description': "Показывает одну задачу",
        'responses': {
            '200': "",
            '404': NOT_FOUND
        },
        'example': {
            "404": {
                "detail": "No Task matches the given query"
            }
        }
    },
    'create': {
        'summary': "Создание задачи",
        'description': "Позволяет создать новую задачу.",
        'responses': {
            '201': "",
            '400': VALIDATION_ERROR_DESCRIPTION
        },
        'example': {  
            "400": {
                "deadline": [
                    "Дэдлайн не может быть в прошлом."
                ]
            }
        }
    },
    'update': {
        'summary': "Обновление задачи",
        'description': "Позволяет обновить задачу полностью",
        'responses': {
            '200': "",
            '400': VALIDATION_ERROR_DESCRIPTION,
            '409': CONFLICT_DATA
        },
        'example': {  
            "400": {
                "deadline": [
                    "Дэдлайн не может быть в прошлом."
                ]
            },
            "409": {
                "task_update_conflict": {"task_update_conflict": "Ошибка. Нельзя изменить статус для оцененной и завершенной задачи."},

            }
        }
    },
    'partial_update': {
        'summary': "Обновление отдельных полей задачи",
        'description': "Позволяет обновить одно поле у задачи",
        'responses': {
            '200': "",
            '400': VALIDATION_ERROR_DESCRIPTION,
            '409': CONFLICT_DATA
        },
        'example': {  
            "400": {
                "deadline": [
                    "Дэдлайн не может быть в прошлом."
                ]
            },
            "409": {
                "task_update_conflict": {"task_update_conflict": "Ошибка. Нельзя изменить исполнителя для оцененной и завершенной задачи."},

            }
        }
    },
    'delete': {
        'summary': "Удалить задачу",
        'description': "Позволяет удалить задачу",
        'responses': {
            '204': "",
            '403': "",
            "404": NOT_FOUND
        },
        'example': {
            "403": {
                "detail": ""
            },
            "404": {
                "detail": "No Task matches the given query"
            }
        }
    }
}


COMMENT_TEXTS = {
    'list': {
        "tags": ["Comments"],
        'summary': "Список комментариев к задаче",
        'description': "Получить все комментарии для определенной задачи",
        'responses': {
            '400': VALIDATION_ERROR_DESCRIPTION,
            '404': NOT_FOUND
        },
        'example': {
            "404": {
                "detail": "No Task matches the given query."
            },
            "400": {
                "detail": "Неверный формат task_pk в URI. Ожидаем число."
            }
        }
    },
    'create': {
        "tags": ["Comments"],
        'summary': "Создать комментарий",
        'description': "Добавить новый комментарий к задаче",
        'responses': {
            '201': "",
            '400': VALIDATION_ERROR_DESCRIPTION,
            '404': NOT_FOUND
        },
        'example': {  
            "400": {
                "text": [
                    "This field is required."
                ]
            },
            "404": {
                "detail": "No Task matches the given query."
            }
        }
    },
    'read': {
        "tags": ["Comments"],
        'summary': "Получить комментарий",
        'description': "Получить конкретный комментарий по ID",
        'responses': {
            '200': "",
            '400': VALIDATION_ERROR_DESCRIPTION,
            '404': NOT_FOUND
        },
        'example': {
            "404": {
                "detail": NO_TASK_COMM_TEXT
            },
            "400": {
                "detail": "Передан неверный формат. Ожидаем число."
            }
        }
    },
    'partial_update': {
        "tags": ["Comments"],
        'summary': "Обновить комментарий",
        'description': "Частично обновить комментарий",
        'responses': {
            '200': "",
            '400': "",
            '403': "",
            '404': NOT_FOUND
        },
        'example': {  
            "400": {
                "text": [
                    ""
                ]
            },
            "403": {
                "detail": ""
            },
            "404": {
                "detail": NO_TASK_COMM_TEXT
            }
        }
    },
    'delete': {
        "tags": ["Comments"],
        'summary': "Удалить комментарий",
        'description': "Удалить комментарий",
        'responses': {
            '204': "",
            '403': "",
            '404': NOT_FOUND
        },
        'example': {
            "403": {
                "detail": ""
            },
            "404": {
                "detail": NO_TASK_COMM_TEXT
            }
        }
    }
}