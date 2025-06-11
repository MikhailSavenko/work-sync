from drf_yasg.openapi import TYPE_STRING, Response as OpenApiResponse, Schema, TYPE_OBJECT, TYPE_STRING, TYPE_ARRAY
from drf_yasg.inspectors.view import SwaggerAutoSchema

from task.doc.texts import TASK_TEXTS, COMMENT_TEXTS, EVALUATION_TEXTS


class TaskAutoSchema(SwaggerAutoSchema):

    def get_operation(self, operation_keys=None):
        operation = super().get_operation(operation_keys)

        if operation_keys and operation_keys[-1] == "list":
            task_text_list = TASK_TEXTS["list"]

            operation.tags = task_text_list["tags"]
            operation.summary = task_text_list["summary"]
            operation.description = task_text_list["description"]
        
        elif operation_keys and operation_keys[-1] == "create":
            task_text_create = TASK_TEXTS["create"]

            operation.tags = task_text_create["tags"]
            operation.summary = task_text_create["summary"]
            operation.description = task_text_create["description"]

            operation.responses["400"] = OpenApiResponse(task_text_create["responses"]["400"], Schema(type=TYPE_OBJECT, properties={"name_field": Schema(type=TYPE_STRING)}, example=task_text_create["example"]["400"]))
        
        elif operation_keys and operation_keys[-1] == "me":
            task_text_me = TASK_TEXTS["me"]

            operation.tags = task_text_me["tags"]
            operation.summary = task_text_me["summary"]
            operation.description = task_text_me["description"]
        
        elif operation_keys and operation_keys[-1] == "read":
            task_text_read = TASK_TEXTS["read"]

            operation.tags = task_text_read["tags"]
            operation.summary = task_text_read["summary"]
            operation.description = task_text_read["description"]

            operation.responses["404"] = OpenApiResponse(task_text_read["responses"]["404"], Schema(type=TYPE_OBJECT, properties={"detail": Schema(type=TYPE_STRING)}, example=task_text_read["example"]["404"]))

        elif operation_keys and operation_keys[-1] == "update":
            task_text_update = TASK_TEXTS["update"]
            
            operation.tags = task_text_update["tags"]
            operation.summary = task_text_update["summary"]
            operation.description = task_text_update["description"]

            operation.responses["400"] = OpenApiResponse(task_text_update["responses"]["400"], Schema(type=TYPE_OBJECT, properties={"name_field": Schema(type=TYPE_STRING)}, example=task_text_update["example"]["400"]))
            operation.responses["409"] = OpenApiResponse(task_text_update["responses"]["409"], Schema(type=TYPE_OBJECT, properties={"task_update_conflict": Schema(type=TYPE_STRING)}, example=task_text_update["example"]["409"]["task_update_conflict"]))
            
        elif operation_keys and operation_keys[-1] == "partial_update":
            task_text_partial_upd = TASK_TEXTS["partial_update"]

            operation.tags = task_text_partial_upd["tags"]
            operation.summary = task_text_partial_upd["summary"]
            operation.description = task_text_partial_upd["description"]

            operation.responses["400"] = OpenApiResponse(task_text_partial_upd["responses"]["400"], Schema(type=TYPE_OBJECT, properties={"name_field": Schema(type=TYPE_STRING)}, example=task_text_partial_upd["example"]["400"]))
            operation.responses["409"] = OpenApiResponse(task_text_partial_upd["responses"]["409"], Schema(type=TYPE_OBJECT, properties={"task_update_conflict": Schema(type=TYPE_STRING)}, example=task_text_partial_upd["example"]["409"]["task_update_conflict"]))

        elif operation_keys and operation_keys[-1] == "delete":
            task_text_delete = TASK_TEXTS["delete"]

            operation.tags = task_text_delete["tags"]
            operation.summary = task_text_delete["summary"]
            operation.description = task_text_delete["description"]
            operation.responses["404"] = OpenApiResponse(task_text_delete["responses"]["404"], Schema(type=TYPE_OBJECT, properties={"detail": Schema(type=TYPE_STRING)}, example=task_text_delete["example"]["404"]))

        return operation


class CommentAutoSchema(SwaggerAutoSchema):

    def get_operation(self, operation_keys=None):
        operation = super().get_operation(operation_keys)

        if operation_keys and operation_keys[-1] == "list":
            comment_text_list = COMMENT_TEXTS["list"]

            operation.tags = comment_text_list["tags"]
            operation.summary = comment_text_list["summary"]
            operation.description = comment_text_list["description"]

            operation.responses["404"] = OpenApiResponse(comment_text_list["responses"]["404"], Schema(type=TYPE_OBJECT, properties={"detail": Schema(type=TYPE_STRING)}, example=comment_text_list["example"]["404"]))
            operation.responses["400"] = OpenApiResponse(comment_text_list["responses"]["400"], Schema(type=TYPE_OBJECT, properties={"detail": Schema(type=TYPE_STRING)}, example=comment_text_list["example"]["400"]))

        elif operation_keys and operation_keys[-1] == "create":
            comment_text_create = COMMENT_TEXTS["create"]

            operation.tags = comment_text_create["tags"]
            operation.summary = comment_text_create["summary"]
            operation.description = comment_text_create["description"]
            
            operation.responses["404"] = OpenApiResponse(comment_text_create["responses"]["404"], Schema(type=TYPE_OBJECT, properties={"detail": Schema(type=TYPE_STRING)}, example=comment_text_create["example"]["404"]))
            operation.responses["400"] = OpenApiResponse(comment_text_create["responses"]["400"], Schema(type=TYPE_OBJECT, properties={"field_name": Schema(type=TYPE_ARRAY, items=Schema(type=TYPE_STRING))}, example=comment_text_create["example"]["400"]))

        elif operation_keys and operation_keys[-1] == "read":
            comment_text_read = COMMENT_TEXTS["read"]
            
            operation.tags = comment_text_read["tags"]
            operation.summary = comment_text_read["summary"]
            operation.description = comment_text_read["description"]

            operation.responses["404"] = OpenApiResponse(comment_text_read["responses"]["404"], Schema(type=TYPE_OBJECT, properties={"detail": Schema(type=TYPE_STRING)}, example=comment_text_read["example"]["404"]))
            operation.responses["400"] = OpenApiResponse(comment_text_read["responses"]["400"], Schema(type=TYPE_OBJECT, properties={"detail": Schema(type=TYPE_ARRAY, items=Schema(type=TYPE_STRING))}, example=comment_text_read["example"]["400"]))

        elif operation_keys and operation_keys[-1] == "partial_update":
            comment_text_partial_upd = COMMENT_TEXTS["partial_update"]

            operation.tags = comment_text_partial_upd["tags"]
            operation.summary = comment_text_partial_upd["summary"]
            operation.description = comment_text_partial_upd["description"]

            operation.responses["404"] = OpenApiResponse(comment_text_partial_upd["responses"]["404"], Schema(type=TYPE_OBJECT, properties={"detail": Schema(type=TYPE_STRING)}, example=comment_text_partial_upd["example"]["404"]))

        elif operation_keys and operation_keys[-1] == "delete":
            comment_text_delete = COMMENT_TEXTS["delete"]

            operation.tags = comment_text_delete["tags"]
            operation.summary = comment_text_delete["summary"]
            operation.description = comment_text_delete["description"]

            operation.responses["404"] = OpenApiResponse(comment_text_delete["responses"]["404"], Schema(type=TYPE_OBJECT, properties={"detail": Schema(type=TYPE_STRING)}, example=comment_text_delete["example"]["404"]))
            
        return operation
    

class EvaluationAutoSchema(SwaggerAutoSchema):

    def get_operation(self, operation_keys=None):
        operation = super().get_operation(operation_keys)

        if operation_keys and operation_keys[-1] == "create":
            evaluation_text_create = EVALUATION_TEXTS["create"]

            operation.tags = evaluation_text_create["tags"]
            operation.summary = evaluation_text_create["summary"]
            operation.description = evaluation_text_create["description"]

            operation.responses["409"] = OpenApiResponse(evaluation_text_create["responses"]["409"], Schema(type=TYPE_OBJECT, properties={"evaluation_create_conflict": Schema(type=TYPE_STRING)}, example=evaluation_text_create["example"]["409"]))
            operation.responses["404"] = OpenApiResponse(evaluation_text_create["responses"]["404"], Schema(type=TYPE_OBJECT, properties={"detail": Schema(type=TYPE_STRING)}, example=evaluation_text_create["example"]["404"]))
            operation.responses["400"] = OpenApiResponse(evaluation_text_create["responses"]["400"], Schema(type=TYPE_OBJECT, properties={"detail": Schema(type=TYPE_ARRAY, items=Schema(type=TYPE_STRING))}, example=evaluation_text_create["example"]["400"]))

        elif operation_keys and operation_keys[-1] == "partial_update":
            evaluation_text_patial_upd = EVALUATION_TEXTS["partial_update"]

            operation.tags = evaluation_text_patial_upd["tags"]
            operation.summary = evaluation_text_patial_upd["summary"]
            operation.description = evaluation_text_patial_upd["description"]

            operation.responses["404"] = OpenApiResponse(evaluation_text_patial_upd["responses"]["404"], Schema(type=TYPE_OBJECT, properties={"detail": Schema(type=TYPE_STRING)}, example=evaluation_text_patial_upd["example"]["404"]))
            operation.responses["400"] = OpenApiResponse(evaluation_text_patial_upd["responses"]["400"], Schema(type=TYPE_OBJECT, properties={"detail": Schema(type=TYPE_ARRAY, items=Schema(type=TYPE_STRING))}, example=evaluation_text_patial_upd["example"]["400"]))
        
        elif operation_keys and operation_keys[-1] == "delete":
            evaluation_text_delete = EVALUATION_TEXTS["delete"]

            operation.tags = evaluation_text_delete["tags"]
            operation.summary = evaluation_text_delete["summary"]
            operation.description = evaluation_text_delete["description"]

            operation.responses["404"] = OpenApiResponse(evaluation_text_delete["responses"]["404"], Schema(type=TYPE_OBJECT, properties={"detail": Schema(type=TYPE_STRING)}, example=evaluation_text_delete["example"]["404"]))
        return operation