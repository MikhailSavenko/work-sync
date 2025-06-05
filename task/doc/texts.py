VALIDATION_ERROR_DESCRIPTION = "Ошибки валидации"

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
            '404': "Задача не найдена"
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
            '403': ""
        },
        'example': {  
            "400": {
                "deadline": [
                    "Дэдлайн не может быть в прошлом."
                ]
            }
        }
    },
    'delete': {
        'summary': "",
        'description': "",
        'responses': {
            '204': "",
            '403': ""
        },
        'example': {
            "403": {
                "detail": ""
            }
        }
    }
}