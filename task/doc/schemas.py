from drf_yasg.openapi import Parameter, IN_QUERY, TYPE_STRING, Response as OpenApiResponse, Schema, TYPE_OBJECT, TYPE_STRING, TYPE_ARRAY
from drf_yasg.inspectors.view import SwaggerAutoSchema

from task.doc.texts import TASK_TEXTS, COMMENT_TEXTS


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
            operation.responses["409"] = OpenApiResponse(TASK_TEXTS["update"]["responses"]["409"], Schema(type=TYPE_OBJECT, properties={"task_update_conflict": Schema(type=TYPE_STRING)}, example=TASK_TEXTS["update"]["example"]["409"]["task_update_conflict"]))
            
        elif operation_keys and operation_keys[-1] == "partial_update":
            operation.summary = TASK_TEXTS["partial_update"]["summary"]
            operation.description = TASK_TEXTS["partial_update"]["description"]

            operation.responses["400"] = OpenApiResponse(TASK_TEXTS["partial_update"]["responses"]["400"], Schema(type=TYPE_OBJECT, properties={"name_field": Schema(type=TYPE_STRING)}, example=TASK_TEXTS["update"]["example"]["400"]))
            operation.responses["409"] = OpenApiResponse(TASK_TEXTS["partial_update"]["responses"]["409"], Schema(type=TYPE_OBJECT, properties={"task_update_conflict": Schema(type=TYPE_STRING)}, example=TASK_TEXTS["partial_update"]["example"]["409"]["task_update_conflict"]))


        elif operation_keys and operation_keys[-1] == "delete":
            operation.summary = TASK_TEXTS["delete"]["summary"]
            operation.description = TASK_TEXTS["delete"]["description"]
            operation.responses["404"] = OpenApiResponse(TASK_TEXTS["read"]["responses"]["404"], Schema(type=TYPE_OBJECT, properties={"detail": Schema(type=TYPE_STRING)}, example=TASK_TEXTS["read"]["example"]["404"]))

        return operation


class CommentAutoSchema(SwaggerAutoSchema):

    def get_operation(self, operation_keys=None):
        operation = super().get_operation(operation_keys)

        print(operation_keys)
        if operation_keys and operation_keys[-1] == "list":
            comment_text_list = COMMENT_TEXTS["list"]

            operation.tags = comment_text_list["tags"]
            operation.summary = comment_text_list["summary"]
            operation.description = comment_text_list["description"]

            operation.responses["404"] = OpenApiResponse(comment_text_list["responses"]["404"], Schema(type=TYPE_OBJECT, properties={"detail": Schema(type=TYPE_STRING)}, example=comment_text_list["example"]["404"]))
            operation.responses["400"] = OpenApiResponse(comment_text_list["responses"]["400"], Schema(type=TYPE_OBJECT, properties={"detail": Schema(type=TYPE_STRING)}, example=comment_text_list["example"]["400"]))

        if operation_keys and operation_keys[-1] == "create":
            comment_text_create = COMMENT_TEXTS["create"]

            operation.tags = comment_text_create["tags"]
            operation.summary = comment_text_create["summary"]
            operation.description = comment_text_create["description"]
            
            operation.responses["404"] = OpenApiResponse(comment_text_create["responses"]["404"], Schema(type=TYPE_OBJECT, properties={"detail": Schema(type=TYPE_STRING)}, example=comment_text_create["example"]["404"]))
            operation.responses["400"] = OpenApiResponse(comment_text_create["responses"]["400"], Schema(type=TYPE_OBJECT, properties={"field_name": Schema(type=TYPE_ARRAY, items=Schema(type=TYPE_STRING))}, example=comment_text_create["example"]["400"]))

        if operation_keys and operation_keys[-1] == "read":
            comment_text_read = COMMENT_TEXTS["read"]
            
            operation.tags = comment_text_read["tags"]
            operation.summary = comment_text_read["summary"]
            operation.description = comment_text_read["description"]

            operation.responses["404"] = OpenApiResponse(comment_text_read["responses"]["404"], Schema(type=TYPE_OBJECT, properties={"detail": Schema(type=TYPE_STRING)}, example=comment_text_read["example"]["404"]))
            operation.responses["400"] = OpenApiResponse(comment_text_read["responses"]["400"], Schema(type=TYPE_OBJECT, properties={"detail": Schema(type=TYPE_ARRAY, items=Schema(type=TYPE_STRING))}, example=comment_text_read["example"]["400"]))

        if operation_keys and operation_keys[-1] == "partial_update":
            comment_text_partial_upd = COMMENT_TEXTS["partial_update"]

            operation.tags = comment_text_partial_upd["tags"]
            operation.summary = comment_text_partial_upd["summary"]
            operation.description = comment_text_partial_upd["description"]

            operation.responses["404"] = OpenApiResponse(comment_text_partial_upd["responses"]["404"], Schema(type=TYPE_OBJECT, properties={"detail": Schema(type=TYPE_STRING)}, example=comment_text_partial_upd["example"]["404"]))

        if operation_keys and operation_keys[-1] == "delete":
            comment_text_delete = COMMENT_TEXTS["delete"]

            operation.tags = comment_text_delete["tags"]
            operation.summary = comment_text_delete["summary"]
            operation.description = comment_text_delete["description"]

            operation.responses["404"] = OpenApiResponse(comment_text_delete["responses"]["404"], Schema(type=TYPE_OBJECT, properties={"detail": Schema(type=TYPE_STRING)}, example=comment_text_delete["example"]["404"]))
            
        return operation