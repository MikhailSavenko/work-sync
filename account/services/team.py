from account.models import Worker


def get_worker_with_team(workers: list[Worker]) -> list[Worker]:
    """Вернет сотрудников, если у них уже есть команда"""
    return [worker for worker in workers if worker.team is not None]
