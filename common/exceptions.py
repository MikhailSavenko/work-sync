from rest_framework.views import exception_handler
from common.variables import NO_TASK, NO_WORKER, NO_MEETING, NO_COMMENT, NO_EVALUATION, NO_TEAM, NO_VALID_STRING, NOT_VALID_TOKEN

ERROR_TRANSLATIONS = {
    # 404 ошибки
    "No Task matches the given query.": NO_TASK,
    "No Worker matches the given query.": NO_WORKER,
    "No Team matches the given query.": NO_TEAM,
    "No Comment matches the given query.": NO_COMMENT,
    "No Evaluation matches the given query.": NO_EVALUATION,
    "No Meeting matches the given query.": NO_MEETING,
    
    "Not a valid string.": NO_VALID_STRING,
    
    "Given token not valid for any token type": NOT_VALID_TOKEN
}


def translate_error_message(message: str):
    """
    Переводит сообщение об ошибке, используя словарь переводов.
    """
    message_str = str(message)

    if message_str in ERROR_TRANSLATIONS:
        return ERROR_TRANSLATIONS[message_str]

    return message_str


def custom_exception_handler(exc, context):

    response = exception_handler(exc, context)

    if response is not None:
        
        data = response.data
        
        if isinstance(data, dict):
            if "detail" in data:
                data["detail"] = translate_error_message(data["detail"])

            for field, errors in data.items():
                if field != "detail" and isinstance(errors, list):
                    data[field] = [translate_error_message(error) for error in errors]

    return response