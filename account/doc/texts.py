VALIDATION_ERROR_DESCRIPTION = "Ошибка валидации"
NOT_FOUND_DESCRIPTION = "Объект не найден"
FORBIDDEN_DESCRIPTION = "Доступ запрещен"
CONFLICT_DATA = "Конфликт данных"

TAGS_TEAMS = ["Teams"]
NO_TEAMS = "No Team matches the given query"

TEAM_TEXTS = {
    'list': {
        "tags": TAGS_TEAMS,
        'summary': "Список всех команд",
        'description': "Список всех команд на площадке",
        'responses': {
            '200': ""
        }
    },
    'read': {
        "tags": TAGS_TEAMS,
        'summary': "Получить команду по ID",
        'description': "Детальная информация о конкретной команде",
        'responses': {
            '200': "",
            '404': NOT_FOUND_DESCRIPTION
        },
        'example' : {
            "404": {
            "detail": NO_TEAMS
        }
        }

    },
    'create': {
        "tags": TAGS_TEAMS,
        'summary': "Создание новой команды",
        'description': "Позволяет создать новую команду с указанными параметрами. Возвращает созданный объект команды.",
        'responses': {
            '201': "",
            '400': VALIDATION_ERROR_DESCRIPTION,
            "409": CONFLICT_DATA
        },
        'example': {
            "400": {
                "title": ["Not a valid string."]
            },
            "409": {
                "detail": "Конфликт. Сотрудники ['mi47sav4@gmail.com'], добавляемые в команду, уже состоят в других командах"
            }
        }
        
    },
    'update': {
        "tags": TAGS_TEAMS,
        'summary': "Изменение команды",
        'description': "Позволяет изменить существующую команду",
        'responses': {
            '400': VALIDATION_ERROR_DESCRIPTION,
            '403': FORBIDDEN_DESCRIPTION,
            "409": CONFLICT_DATA
        },
        'example': {
            "400": {
                "title": ["Not a valid string."]
            },
            "409": {
                "detail": "Конфликт. Сотрудники ['mi47sav4@gmail.com'], добавляемые в команду, уже состоят в других командах"
            }
        }
    },
    'delete': {
        "tags": TAGS_TEAMS,
        'summary': "Удаление команды",
        'description': "Позволяет удалить существующую команду",
        'responses': {
            "404": NOT_FOUND_DESCRIPTION,
            '403': FORBIDDEN_DESCRIPTION
        },
        'example': {
            "403": {"detail": "Удаление команды возможна только ее создателем."},
            "404": {"detail": NO_TEAMS}
        }
}
}