from drf_yasg.openapi import Parameter, TYPE_STRING, IN_PATH, Response as OpenApiResponse, Schema, TYPE_OBJECT, TYPE_STRING, TYPE_ARRAY
from drf_yasg.inspectors.view import SwaggerAutoSchema

from account.doc.texts import TEAM_TEXTS, WORKER_TEXTS

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


class WorkerAutoSchema(SwaggerAutoSchema):

    def get_operation(self, operation_keys=None):
        operation = super().get_operation(operation_keys)
        print(operation_keys)
        if operation_keys and operation_keys[-1] == "list":
            worker_text_list = WORKER_TEXTS["list"]

            operation.tags = worker_text_list["tags"]
            operation.summary = worker_text_list["summary"]
            operation.description = worker_text_list["description"]

        elif operation_keys and operation_keys[-1] == "read":
            worker_text_read = WORKER_TEXTS["read"]

            operation.tags = worker_text_read["tags"]
            operation.summary = worker_text_read["summary"]
            operation.description = worker_text_read["description"]

            operation.responses["404"] = OpenApiResponse(worker_text_read["responses"]["404"], Schema(type=TYPE_OBJECT, properties={"detail": Schema(type=TYPE_STRING, description=worker_text_read["responses"]["404"])}, example=worker_text_read["example"]["404"]))
        
        elif operation_keys and operation_keys[-1] == "partial_update":
            worker_text_partial_upd = WORKER_TEXTS["partial_update"]
            
            operation.tags = worker_text_partial_upd["tags"]
            operation.summary = worker_text_partial_upd["summary"]
            operation.description = worker_text_partial_upd["description"]
          
            operation.responses["400"] = OpenApiResponse(worker_text_partial_upd["responses"]["400"], Schema(type=TYPE_OBJECT, properties={"name_field": Schema(type=TYPE_ARRAY, items=Schema(type=TYPE_STRING))}, example=worker_text_partial_upd["example"]["400"]))

        elif operation_keys and operation_keys[-1] == "calendar_day":
            worker_text_calendar_day = WORKER_TEXTS["calendar_day"]

            operation.tags = worker_text_calendar_day["tags"]
            operation.summary = worker_text_calendar_day["summary"]
            operation.description = worker_text_calendar_day["description"]
            print(operation.parameters)
            operation.parameters.append(
                Parameter(
                    "date", # Название параметра, как в url_path
                    IN_PATH, # Тип параметра (в пути)
                    type=TYPE_STRING, # Тип данных
                    format="date", # для дат
                    description="Дата в формате ГГГГ-ММ-ДД", # Четкое описание формата
                    example="2025-06-10" # Пример значения для поля в Swagger UI
                )
            )
            operation.responses["404"] = OpenApiResponse(worker_text_calendar_day["responses"]["404"], Schema(type=TYPE_OBJECT, properties={"detail": Schema(type=TYPE_STRING, description=worker_text_calendar_day["responses"]["404"])}, example=worker_text_calendar_day["example"]["404"]))
        return operation