from account.models import Worker


def get_worker_with_team(workers: list[Worker]) -> list[Worker]:
    """Вернет сотрудников, если у них уже есть команда"""
    return [worker for worker in workers if worker.team is not None]


def is_your_team(team_pk: str, worker: Worker) -> bool:
    """
    Проверяет, состоит ли сотрудник в команде с указанным ID.

    Функция сравнивает ID команды, к которой прикреплен работник,
    с предоставленным ID команды. Если у работника нет команды,
    функция возвращает False.

    :param team_pk: Строковый идентификатор (Primary Key) команды для сравнения.
    :param worker: Экземпляр модели Worker, чье членство в команде проверяется.
    :return: True, если работник является членом указанной команды; иначе False.
    """
    if worker.team is None:
        return False
    
    return int(team_pk) == worker.team.id