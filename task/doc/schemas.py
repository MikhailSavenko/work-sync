from drf_yasg.openapi import Parameter, IN_QUERY, TYPE_STRING, Response as OpenApiResponse, Schema, TYPE_OBJECT, TYPE_STRING, TYPE_ARRAY
from drf_yasg.inspectors.view import SwaggerAutoSchema

from task.doc.texts import TASK_TEXTS


class TaskAutoSchema(SwaggerAutoSchema):

    def get_operation(self, operation_keys=None):
        operation = super().get_operation(operation_keys)

        if operation_keys and operation_keys[-1] == "list":
            operation.summary = TASK_TEXTS["list"]["summary"]
            operation.description = TASK_TEXTS["list"]["description"]
        
        elif operation_keys and operation_keys[-1] == "create":
            operation.summary = TASK_TEXTS["create"]["summary"]
            operation.description = TASK_TEXTS["create"]["description"]

            operation.responses["400"] = OpenApiResponse(TASK_TEXTS["create"]["responses"]["400"], Schema(type=TYPE_OBJECT, properties={"name_field": Schema(type=TYPE_STRING)}, example=TASK_TEXTS["create"]["example"]["400"]))
        
        elif operation_keys and operation_keys[-1] == "me":
            operation.summary = TASK_TEXTS["me"]["summary"]
            operation.description = TASK_TEXTS["me"]["description"]
        
        elif operation_keys and operation_keys[-1] == "read":
            operation.summary = TASK_TEXTS["read"]["summary"]
            operation.description = TASK_TEXTS["read"]["description"]

            operation.responses["404"] = OpenApiResponse(TASK_TEXTS["read"]["responses"]["404"], Schema(type=TYPE_OBJECT, properties={"detail": Schema(type=TYPE_STRING)}, example=TASK_TEXTS["read"]["example"]["404"]))

        elif operation_keys and operation_keys[-1] == "update":
            operation.summary = TASK_TEXTS["update"]["summary"]
            operation.description = TASK_TEXTS["update"]["description"]

            operation.responses["400"] = OpenApiResponse(TASK_TEXTS["update"]["responses"]["400"], Schema(type=TYPE_OBJECT, properties={"name_field": Schema(type=TYPE_STRING)}, example=TASK_TEXTS["update"]["example"]["400"]))
        
        elif operation_keys and operation_keys[-1] == "partial_update":
            operation.summary = TASK_TEXTS["partial_update"]["summary"]
            operation.description = TASK_TEXTS["partial_update"]["description"]

            operation.responses["400"] = OpenApiResponse(TASK_TEXTS["partial_update"]["responses"]["400"], Schema(type=TYPE_OBJECT, properties={"name_field": Schema(type=TYPE_STRING)}, example=TASK_TEXTS["update"]["example"]["400"]))
        
        elif operation_keys and operation_keys[-1] == "delete":
            operation.summary = TASK_TEXTS["delete"]["summary"]
            
        return operation