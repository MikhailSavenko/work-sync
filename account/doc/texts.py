from common.variables import INVALID_PASSWORD, TEAM_WORKER_CONFLICT, VALIDATION_ERROR_DESCRIPTION, UNAUTHORIZED_REQUEST, FORBIDDEN_403_RUSSIAN, CONFLICT_DATA, NOT_FOUND_DESCRIPTION, FORBIDDEN_DESCRIPTION, NO_VALID_STRING, NO_TEAM, NO_WORKER, NO_ACTIVE_ACCOUNT, NOT_VALID_TOKEN_FOR_ANY_TOKEN_TYPE, REQUIRED_FIELD, TOKEN_BLACKLISTED, TOKEN_IS_INVALID

TAGS_TEAMS = ["Teams"]
TAGS_WORKER = ["Workers"]
TAGS_AUTH = ["Auth"]

CODE_TOKEN_NOT_VALID = "token_not_valid"


TEAM_TEXTS = {
    "list": {
        "tags": TAGS_TEAMS,
        "summary": "Список всех команд",
        "description": "Список всех команд на площадке",
        "responses": {"200": ""},
    },
    "read": {
        "tags": TAGS_TEAMS,
        "summary": "Получить команду по ID",
        "description": "Детальная информация о конкретной команде",
        "responses": {"200": "", "404": NOT_FOUND_DESCRIPTION},
        "example": {"404": {"detail": NO_TEAM}},
    },
    "create": {
        "tags": TAGS_TEAMS,
        "summary": "Создание новой команды",
        "description": "Позволяет создать новую команду с указанными параметрами. Возвращает созданный объект команды.",
        "responses": {"403": FORBIDDEN_DESCRIPTION, "400": VALIDATION_ERROR_DESCRIPTION, "409": CONFLICT_DATA},
        "example": {
            "400": {"title": [NO_VALID_STRING]},
            "409": {
                "detail": TEAM_WORKER_CONFLICT
            },
            "403": {"detail": FORBIDDEN_403_RUSSIAN},
        },
    },
    "update": {
        "tags": TAGS_TEAMS,
        "summary": "Изменение команды",
        "description": "Позволяет изменить существующую команду",
        "responses": {"400": VALIDATION_ERROR_DESCRIPTION, "404": NOT_FOUND_DESCRIPTION, "403": FORBIDDEN_DESCRIPTION, "409": CONFLICT_DATA},
        "example": {
            "400": {"title": [NO_VALID_STRING]},
            "409": {
                "detail": TEAM_WORKER_CONFLICT
            },
            "403": {"detail": FORBIDDEN_403_RUSSIAN},
            "404": {"detail": NO_TEAM}
        },
    },
    "delete": {
        "tags": TAGS_TEAMS,
        "summary": "Удаление команды",
        "description": "Позволяет удалить существующую команду",
        "responses": {"404": NOT_FOUND_DESCRIPTION, "403": FORBIDDEN_DESCRIPTION},
        "example": {"403": FORBIDDEN_403_RUSSIAN, "404": {"detail": NO_TEAM}},
    },
}


WORKER_TEXTS = {
    "list": {
        "tags": TAGS_WORKER,
        "summary": "Список всех сотрудников",
        "description": "Список всех сотрудников на площадке",
        "responses": {"200": ""},
    },
    "read": {
        "tags": TAGS_WORKER,
        "summary": "Получить сотрудника по ID",
        "description": "Детальная информация о конкретном сотруднике",
        "responses": {"200": "", "404": NOT_FOUND_DESCRIPTION},
        "example": {"404": {"detail": NO_WORKER}},
    },
    "calendar_day": {
        "tags": TAGS_WORKER,
        "summary": "События сотрудника на день",
        "description": "Показывает события сотрудника за определенный день",
        "responses": {
            "200": "",
            "404": NOT_FOUND_DESCRIPTION,
        },
        "example": {"404": {"detail": NO_WORKER}},
    },
    "calendar_month": {
        "tags": TAGS_WORKER,
        "summary": "События сотрудника на месяц",
        "description": "Показывает события сотрудника за определенный месяц. События показывают за введенный полный месяц.",
        "responses": {
            "200": "",
            "404": NOT_FOUND_DESCRIPTION,
        },
        "example": {"404": {"detail": NO_WORKER}},
    },
    "average_evaluation": {
        "tags": TAGS_WORKER,
        "summary": "Средняя оценка сотрудника",
        "description": "Показывает среднюю оценка сотрудника за введенный период",
        "responses": {
            "200": "",
            "404": NOT_FOUND_DESCRIPTION,
        },
        "example": {"404": {"detail": NO_WORKER}},
    },
    "partial_update": {
        "tags": TAGS_WORKER,
        "summary": "Изменение роли сотрудника",
        "description": "Позволяет изменить роль сотрудника",
        "responses": {
            "400": VALIDATION_ERROR_DESCRIPTION,
            "403": FORBIDDEN_DESCRIPTION,
            "404": NOT_FOUND_DESCRIPTION,
        },
        "example": {"400": {"status": ['Значения "NfM" нет среди допустимых вариантов.']}, "403": {"detail": FORBIDDEN_403_RUSSIAN}, "404": {"detail": NO_WORKER}},
    },
}


TOKEN_OBTAIN_TEXTS = {
    "create": {
        "tags": TAGS_AUTH,
        "summary": "Аутентификация",
        "description": "Получение токенов по введенным данным",
        "responses": {"200": "Успешная аутентификация", "401": UNAUTHORIZED_REQUEST},
        "example": {
            "401": {"detail": NO_ACTIVE_ACCOUNT},
            "200": {
                "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc1MDE3Mjc0NywiaWF0IjoxNzQ5NTY3OTQ3LCJqdGkiOiIyYTVjZTJlODllMjI0M2E2YmNiMjg1OTg0MjQwYTRmZiIsInVzZXJfaWQiOjh9.7Rqk9H07m4OHmnUdU6B0n09bXzj8tF6w_GD04mRc7QU",
                "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc1MDE3Mjc0NywiaWF0IjoxNzQ5NTY3OTQ3LCJqdGkiOiIyYTVjZTJlODllMjI0M2E2YmNiMjg1OTg0MjQwYTRmZiIsInVzZXJfaWQiOjh9.7Rqk9H07m4OHmnUdU6B0n09bXzj8tF6w_GD04mRc7QU",
            },
        },
    }
}


TOKEN_BLACKLIST_TEXTS = {
    "create": {
        "tags": TAGS_AUTH,
        "summary": "Аннулирование токена обновления",
        "description": "Добавляет предоставленный токен обновления в черный список, делая его недействительным для дальнейшего использования",
        "responses": {"200": "Успешное аннулирование токена", "401": UNAUTHORIZED_REQUEST},
        "example": {"401": {"detail": TOKEN_BLACKLISTED, "code": CODE_TOKEN_NOT_VALID}},
    }
}


TOKEN_REFRESH_TEXTS = {
    "create": {
        "tags": TAGS_AUTH,
        "summary": "Обновить пару токенов доступа и обновления",
        "description": "Принимает токен обновления и возвращает новую пару токенов доступа",
        "responses": {"200": "Успешное обновление токенов", "401": UNAUTHORIZED_REQUEST},
        "example": {
            "401": {"detail": TOKEN_BLACKLISTED, "code": CODE_TOKEN_NOT_VALID},
            "200": {
                "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc1MDE3Mjc0NywiaWF0IjoxNzQ5NTY3OTQ3LCJqdGkiOiIyYTVjZTJlODllMjI0M2E2YmNiMjg1OTg0MjQwYTRmZiIsInVzZXJfaWQiOjh9.7Rqk9H07m4OHmnUdU6B0n09bXzj8tF6w_GD04mRc7QU",
                "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc1MDE3Mjc0NywiaWF0IjoxNzQ5NTY3OTQ3LCJqdGkiOiIyYTVjZTJlODllMjI0M2E2YmNiMjg1OTg0MjQwYTRmZiIsInVzZXJfaWQiOjh9.7Rqk9H07m4OHmnUdU6B0n09bXzj8tF6w_GD04mRc7QU",
            },
        },
    }
}


TOKEN_VERIFY_TEXTS = {
    "create": {
        "tags": TAGS_AUTH,
        "summary": "Проверить валидность JWT-токена (доступ или обновление)",
        "description": "Принимает любой JWT-токен (как доступа, так и обновления) и указывает, является ли он действительным (не истекшим, не поврежденным, с корректной подписью). Этот эндпоинт не предоставляет информацию о типе токена (access/refresh) и не проверяет полномочия для конкретных действий или доступ к ресурсам.",
        "responses": {"200": "Токен валиден", "401": "Токен недействителен или просрочен", "400": "Токен в блэклисте"},
        "example": {
            "401": {"detail": TOKEN_IS_INVALID, "code": CODE_TOKEN_NOT_VALID},
            "200": {},
            "400": {"non_field_errors": [TOKEN_BLACKLISTED]},
        },
    }
}


USER_REGISTER_TEXTS = {
    "create": {
        "tags": TAGS_AUTH,
        "summary": "Регистрация",
        "description": "Создание аккаунта на площадке. Создаем модель User, а также Worker создается автоматически и имеет связь с User OneToOne.",
        "responses": {"201": "Успешная регистрация", "400": VALIDATION_ERROR_DESCRIPTION},
        "example": {"201": {"email": "user@example.com", "id": 0}, "400": {"email": ["Введите правильный адрес электронной почты."]}},
    },
    "me_update": {
        "tags": TAGS_AUTH,
        "summary": "Обновление данных аккаунта",
        "description": "Позволяет обновить данные вашего аккаунта",
        "responses": {"400": VALIDATION_ERROR_DESCRIPTION},
        "example": {"400": {"email": [REQUIRED_FIELD]}},
    },
    "me_delete": {
        "tags": TAGS_AUTH,
        "summary": "Удаление аккаунта",
        "description": "Позволяет удалить аккаунт. Удаляет User, а такде Worker сущности.",
        "responses": {
            "204": "Успешное удаление",
            "400": VALIDATION_ERROR_DESCRIPTION,
            "401": UNAUTHORIZED_REQUEST,
        },
        "example": {
            "401": {"detail": NOT_VALID_TOKEN_FOR_ANY_TOKEN_TYPE, "code": "token_not_valid"},
            "400": {"current_password": [INVALID_PASSWORD]},
        },
    },
}
