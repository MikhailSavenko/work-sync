from drf_yasg.openapi import Parameter, IN_QUERY, TYPE_STRING, Response as OpenApiResponse, Schema, TYPE_OBJECT, TYPE_STRING, TYPE_ARRAY
from drf_yasg.inspectors.view import SwaggerAutoSchema

from event.serializers import MeetingGetSerializer


class MeetingAutoSchema(SwaggerAutoSchema):

    def get_operation(self, operation_keys=None):
        operation = super().get_operation(operation_keys)

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
        return operation