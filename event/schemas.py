from drf_yasg.openapi import Parameter, IN_QUERY, TYPE_STRING, Response as OpenApiResponse, Schema, TYPE_OBJECT, TYPE_STRING, TYPE_ARRAY
from drf_yasg.inspectors.view import SwaggerAutoSchema

from event.serializers import MeetingCreateUpdateSerializer, MeetingGetSerializer


class MeetingAutoSchema(SwaggerAutoSchema):

    VALIDATION_ERROR_SCHEMA = Schema(type=TYPE_OBJECT, properties={
                "non_field_errors": Schema(type=TYPE_ARRAY, items=Schema(type=TYPE_STRING), description="Общие ошибки валидации")
            }, example={
        "non_field_errors": ["Сообщение об ошибке"]
    })

    def get_operation(self, operation_keys=None):
        operation = super().get_operation(operation_keys)
        print(operation_keys)
        # дока для me
        if operation_keys and operation_keys[-1] == "me":
            operation.summary = "Получение встреч пользователя"
            operation.description = "Встречи в которых участвует сотрудник"
            operation.parameters.append(
                Parameter(
                    "done",
                    IN_QUERY,
                    description="Фильтр встреч по времени (0 - предстоящие, 1 - все, включая прошедшие)",
                    type=TYPE_STRING,
                    enum=["0", "1"],
                    default="0",
                )
            )
            operation.responses = {
                "200": OpenApiResponse("Список встреч", Schema(type=TYPE_ARRAY, items=self.serializer_to_schema(MeetingGetSerializer()))),
                "400": OpenApiResponse("Некорректный параметр done", Schema(type=TYPE_OBJECT, properties={"error": Schema(type=TYPE_STRING)}))
            }

        elif operation_keys and operation_keys[-1] == "list":
            operation.summary = "Список всех встреч"
            operation.description = "Список всех встреч на площидке и предстоящщие и прошедшие"
            operation.responses = {
                "200": OpenApiResponse("Список встреч", Schema(type=TYPE_ARRAY, items=self.serializer_to_schema(MeetingGetSerializer()))),
            }
        
        elif operation_keys and operation_keys[-1] == "read":
            operation.summary = "Получить встречу по ID"
            operation.description = "Определенная встреча"
            operation.responses = {
                "200": OpenApiResponse("Встреча", self.serializer_to_schema(MeetingGetSerializer())),
                "404": OpenApiResponse("Встреча не найдена", Schema(type=TYPE_OBJECT, properties={"detail": Schema(type=TYPE_STRING, description="Встреча не найдена")}))
            }

        elif operation_keys and operation_keys[-1] == "create":
            operation.summary = "Создание новой встречи"
            operation.description = "Позволяет создать новую встречу с указанными параметрами. Возвращает созданный объект встречи."
            operation.request_body = self.get_request_body_schema(MeetingCreateUpdateSerializer())
            
            operation.responses["400"] = OpenApiResponse(description="Ошибки валидации", schema=self.VALIDATION_ERROR_SCHEMA)
        
        elif operation_keys and operation_keys[-1] == "update":
            operation.summary = "Изменение встречи"
            operation.description = "Позволяет изменить существующую встречу"
            operation.request_body = self.get_request_body_schema(MeetingCreateUpdateSerializer())
            
            operation.responses["400"] = OpenApiResponse(description="Ошибки валидации", schema=self.VALIDATION_ERROR_SCHEMA)
        
        elif operation_keys and operation_keys[-1] == "delete":
            operation.summary = "Отмена встречи"
            operation.description = "Позволяет удалить существующую встречу"

            operation.responses["403"] = OpenApiResponse(description="Доступ запрещен", schema=Schema(type=TYPE_OBJECT, properties={"detail": Schema(type=TYPE_STRING, description="Отмена встречи возможна только ее создателем.")}, example={
    "detail": "Отмена встречи возможна только ее создателем."
}))
        return operation