VALIDATION_ERROR_DESCRIPTION = "Ошибки валидации"
CONFLICT_DATA = "Конфликт данных"
TASK_NOT_FOUND = "Задача не найдена"
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
            '404': TASK_NOT_FOUND
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
            "404": TASK_NOT_FOUND
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