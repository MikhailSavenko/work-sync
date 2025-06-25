from rest_framework.exceptions import ValidationError

from common.variables import SENT_INVALID_FORMAT


def is_int_or_valid_error(num_check: int) -> int | ValidationError:
    try:
        num = int(num_check)
        return num
    except (ValueError, TypeError):
        raise ValidationError({"detail": SENT_INVALID_FORMAT})
