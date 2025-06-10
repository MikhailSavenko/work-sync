VALIDATION_ERROR_DESCRIPTION = "Ошибка валидации"
NOT_FOUND_DESCRIPTION = "Объект не найден"
FORBIDDEN_DESCRIPTION = "Доступ запрещен"
CONFLICT_DATA = "Конфликт данных"

TAGS_TEAMS = ["Teams"]
NO_TEAMS = "No Team matches the given query"

TAGS_WORKER = ["Workers"]
NO_WORKER = "No Worker matches the given query"

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



WORKER_TEXTS = {
    'list': {
        "tags": TAGS_WORKER,
        'summary': "Список всех сотрудников",
        'description': "Список всех сотрудников на площадке",
        'responses': {
            '200': ""
        }
    },
    'read': {
        "tags": TAGS_WORKER,
        'summary': "Получить сотрудника по ID",
        'description': "Детальная информация о конкретном сотруднике",
        'responses': {
            '200': "",
            '404': NOT_FOUND_DESCRIPTION
        },
        'example' : {
            "404": {
            "detail": NO_WORKER
        }
        }

    },
    'calendar_day': {
        "tags": TAGS_WORKER,
        'summary': "События сотрудника на день",
        'description': "Показывает события сотрудника за определенный день",
        'responses': {
            "200": "",
            '404': NOT_FOUND_DESCRIPTION,
        },
        'example': {
            
            "404": {
                "detail": NO_WORKER
            }
        }
        
    },
    'calendar_month': {
        "tags": TAGS_WORKER,
        'summary': "События сотрудника на месяц",
        'description': "Показывает события сотрудника за определенный месяц. События показывают за введенный полный месяц.",
        'responses': {
            "200": "",
            '404': NOT_FOUND_DESCRIPTION,
        },
        'example': {
            
            "404": {
                "detail": NO_WORKER
            }
        }
        
    },
    'average_evaluation': {
        "tags": TAGS_WORKER,
        'summary': "Средняя оценка сотрудника",
        'description': "Показывает среднюю оценка сотрудника за введенный период",
        'responses': {
            "200": "",
            '404': NOT_FOUND_DESCRIPTION,
        },
        'example': {
            
            "404": {
                "detail": NO_WORKER
            }
        }
        
    },
    'partial_update': {
        "tags": TAGS_WORKER,
        'summary': "Изменение роли сотрудника",
        'description': "Позволяет изменить роль сотрудника",
        'responses': {
            '400': VALIDATION_ERROR_DESCRIPTION,
            '403': FORBIDDEN_DESCRIPTION,

        },
        'example': {
            "400": {
                "status": ["\"NfM\" is not a valid choice."]
            }
        }
    }
}