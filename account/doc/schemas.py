from drf_yasg.openapi import TYPE_STRING, Response as OpenApiResponse, Schema, TYPE_OBJECT, TYPE_STRING, TYPE_ARRAY
from drf_yasg.inspectors.view import SwaggerAutoSchema

from account.doc.texts import TEAM_TEXTS


class TeamAutoSchema(SwaggerAutoSchema):

    def get_operation(self, operation_keys=None):
        operation = super().get_operation(operation_keys)
        
        if operation_keys and operation_keys[-1] == "list":
            team_text_list = TEAM_TEXTS["list"]

            operation.tags = team_text_list["tags"]
            operation.summary = team_text_list["summary"]
            operation.description = team_text_list["description"]
        
        elif operation_keys and operation_keys[-1] == "read":
            team_text_read = TEAM_TEXTS["read"]

            operation.tags = team_text_read["tags"]
            operation.summary = team_text_read["summary"]
            operation.description = team_text_read["description"]

            operation.responses["404"] = OpenApiResponse(team_text_read["responses"]["404"], Schema(type=TYPE_OBJECT, properties={"detail": Schema(type=TYPE_STRING, description=team_text_read["responses"]["404"])}, example=team_text_read["example"]["404"]))
            
        elif operation_keys and operation_keys[-1] == "create":
            team_text_create = TEAM_TEXTS["create"]

            operation.tags = team_text_create["tags"]
            operation.summary = team_text_create["summary"]
            operation.description = team_text_create["description"]
            
            operation.responses["400"] = OpenApiResponse(team_text_create["responses"]["400"], Schema(type=TYPE_OBJECT, properties={"name_field": Schema(type=TYPE_ARRAY, items=Schema(type=TYPE_STRING))}, example=team_text_create["example"]["400"]))
            operation.responses["409"] = OpenApiResponse(team_text_create["responses"]["409"], Schema(type=TYPE_OBJECT, properties={"detail": Schema(type=TYPE_STRING, description=team_text_create["responses"]["409"])}, example=team_text_create["example"]["409"]))
        
        elif operation_keys and operation_keys[-1] == "update":
            team_text_update = TEAM_TEXTS["update"]
            
            operation.tags = team_text_update["tags"]
            operation.summary = team_text_update["summary"]
            operation.description = team_text_update["description"]
          
            operation.responses["400"] = OpenApiResponse(team_text_update["responses"]["400"], Schema(type=TYPE_OBJECT, properties={"name_field": Schema(type=TYPE_ARRAY, items=Schema(type=TYPE_STRING))}, example=team_text_update["example"]["400"]))
            operation.responses["409"] = OpenApiResponse(team_text_update["responses"]["409"], Schema(type=TYPE_OBJECT, properties={"detail": Schema(type=TYPE_STRING, description=team_text_update["responses"]["409"])}, example=team_text_update["example"]["409"]))

        elif operation_keys and operation_keys[-1] == "delete":
            team_text_delete = TEAM_TEXTS["delete"]

            operation.tags = team_text_delete["tags"]
            operation.summary = team_text_delete["summary"]
            operation.description = team_text_delete["description"]

            operation.responses["403"] = OpenApiResponse(team_text_delete["responses"]["403"], schema=Schema(type=TYPE_OBJECT, properties={"detail": Schema(type=TYPE_STRING, description=team_text_delete["responses"]["403"])}, example=team_text_delete["example"]["403"]))
            operation.responses["404"] = OpenApiResponse(team_text_delete["responses"]["404"], Schema(type=TYPE_OBJECT, properties={"detail": Schema(type=TYPE_STRING, description=team_text_delete["responses"]["404"])}, example=team_text_delete["example"]["404"]))
        return operation