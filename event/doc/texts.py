# Общие тексты
VALIDATION_ERROR_DESCRIPTION = "Ошибка валидации"
NOT_FOUND_DESCRIPTION = "Объект не найден"
FORBIDDEN_DESCRIPTION = "Доступ запрещен"
CONFLICT_DATA = "Конфликт данных"
TAGS_MEETINGS = ["Meetings"]
NO_MEETINGS = "No Meeting matches the given query"

# Тексты для MeetingAutoSchema
MEETING_TEXTS = {
    'me': {
        "tags": TAGS_MEETINGS,
        'summary': "Получение встреч пользователя",
        'description': "Встречи в которых участвует сотрудник",
        'done_param': {
            'description': "Фильтр встреч по времени (0 - предстоящие, 1 - все, включая прошедшие)",
            'enum': ["0", "1"],
            'default': "0"
        },
        'responses': {
            '200': "Список встреч",
            '400': "Некорректный параметр done"
        },
        'example': {
            "400": {
                "detail": "Парамтер 'done' может быть 0 или 1"
            }
        }
    },
    'list': {
        "tags": TAGS_MEETINGS,
        'summary': "Список всех встреч",
        'description': "Список всех встреч на площадке: и предстоящие и прошедшие",
        'responses': {
            '200': "Список встреч"
        }
    },
    'read': {
        "tags": TAGS_MEETINGS,
        'summary': "Получить встречу по ID",
        'description': "Детальная информация о конкретной встрече",
        'responses': {
            '200': "Встреча",
            '404': NOT_FOUND_DESCRIPTION
        },
        'example' : {
            "404": {
            "detail": NO_MEETINGS
        }
        }

    },
    'create': {
        "tags": TAGS_MEETINGS,
        'summary': "Создание новой встречи",
        'description': "Позволяет создать новую встречу с указанными параметрами. Возвращает созданный объект встречи.",
        'responses': {
            '201': "Встреча создана",
            '400': VALIDATION_ERROR_DESCRIPTION,
            "409": CONFLICT_DATA
        },
        'example': {
            "400": {
                "description": ["Not a valid string."]
            },
            "409": {
                "detail": "mike@gmail.com уже имеет встречу на дату: 2025-07-05 13:31:00+00:00"
            }
        }
        
    },
    'update': {
        "tags": TAGS_MEETINGS,
        'summary': "Изменение встречи",
        'description': "Позволяет изменить существующую встречу",
        'responses': {
            '400': VALIDATION_ERROR_DESCRIPTION,
            '403': FORBIDDEN_DESCRIPTION,
            "409": CONFLICT_DATA
        },
        'example': {
            "400": {
                "non_field_errors": ["Встреча должна включать минимум двух участников."]
            },
            "409": {
                "detail": "mike@gmail.com уже имеет встречу на дату: 2025-07-05 13:31:00+00:00"
            }
        }
    },
    'delete': {
        "tags": TAGS_MEETINGS,
        'summary': "Отмена встречи",
        'description': "Позволяет удалить существующую встречу",
        'responses': {
            "404": NOT_FOUND_DESCRIPTION,
            '403': FORBIDDEN_DESCRIPTION
        },
        'example': {
            "403": {"detail": "Отмена встречи возможна только ее создателем."},
            "404": {"detail": NO_MEETINGS}
        }
}
}