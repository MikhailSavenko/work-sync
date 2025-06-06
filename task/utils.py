from rest_framework.exceptions import ValidationError


def is_int_or_valid_error(num_check: int) -> int | ValidationError:
    try:
        num = int(num_check)
        return num
    except (ValueError, TypeError):
        raise ValidationError({"detail": "Передан неверный формат. Ожидаем число."})