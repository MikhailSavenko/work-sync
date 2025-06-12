from drf_yasg.openapi import Parameter, TYPE_STRING, IN_PATH, IN_BODY, Response as OpenApiResponse, Schema, TYPE_OBJECT, TYPE_ARRAY, TYPE_INTEGER
from drf_yasg.inspectors.view import SwaggerAutoSchema

from account.doc.texts import TEAM_TEXTS, WORKER_TEXTS, TOKEN_OBTAIN_TEXTS, TOKEN_BLACKLIST_TEXTS, TOKEN_REFRESH_TEXTS, TOKEN_VERIFY_TEXTS, USER_REGISTER_TEXTS

from doc_common.schemes import get_response_open_api_scheme_with_detail_string_and_example


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
            
            operation.responses["403"] = get_response_open_api_scheme_with_detail_string_and_example(text=team_text_create, status_code=403)
            operation.responses["400"] = OpenApiResponse(team_text_create["responses"]["400"], Schema(type=TYPE_OBJECT, properties={"name_field": Schema(type=TYPE_ARRAY, items=Schema(type=TYPE_STRING))}, example=team_text_create["example"]["400"]))
            operation.responses["409"] = OpenApiResponse(team_text_create["responses"]["409"], Schema(type=TYPE_OBJECT, properties={"detail": Schema(type=TYPE_STRING, description=team_text_create["responses"]["409"])}, example=team_text_create["example"]["409"]))
        
        elif operation_keys and operation_keys[-1] == "update":
            team_text_update = TEAM_TEXTS["update"]
            
            operation.tags = team_text_update["tags"]
            operation.summary = team_text_update["summary"]
            operation.description = team_text_update["description"]

            operation.responses["403"] = get_response_open_api_scheme_with_detail_string_and_example(text=team_text_update, status_code=403)
            operation.responses["400"] = OpenApiResponse(team_text_update["responses"]["400"], Schema(type=TYPE_OBJECT, properties={"name_field": Schema(type=TYPE_ARRAY, items=Schema(type=TYPE_STRING))}, example=team_text_update["example"]["400"]))
            operation.responses["409"] = OpenApiResponse(team_text_update["responses"]["409"], Schema(type=TYPE_OBJECT, properties={"detail": Schema(type=TYPE_STRING, description=team_text_update["responses"]["409"])}, example=team_text_update["example"]["409"]))

        elif operation_keys and operation_keys[-1] == "delete":
            team_text_delete = TEAM_TEXTS["delete"]

            operation.tags = team_text_delete["tags"]
            operation.summary = team_text_delete["summary"]
            operation.description = team_text_delete["description"]

            operation.responses["403"] = get_response_open_api_scheme_with_detail_string_and_example(text=team_text_delete, status_code=403)
            operation.responses["404"] = OpenApiResponse(team_text_delete["responses"]["404"], Schema(type=TYPE_OBJECT, properties={"detail": Schema(type=TYPE_STRING, description=team_text_delete["responses"]["404"])}, example=team_text_delete["example"]["404"]))
        return operation


class WorkerAutoSchema(SwaggerAutoSchema):

    def get_operation(self, operation_keys=None):
        operation = super().get_operation(operation_keys)
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

            operation.responses["403"] = get_response_open_api_scheme_with_detail_string_and_example(text=worker_text_partial_upd, status_code=403)
            operation.responses["400"] = OpenApiResponse(worker_text_partial_upd["responses"]["400"], Schema(type=TYPE_OBJECT, properties={"name_field": Schema(type=TYPE_ARRAY, items=Schema(type=TYPE_STRING))}, example=worker_text_partial_upd["example"]["400"]))

        elif operation_keys and operation_keys[-1] == "calendar_day":
            worker_text_calendar_day = WORKER_TEXTS["calendar_day"]

            operation.tags = worker_text_calendar_day["tags"]
            operation.summary = worker_text_calendar_day["summary"]
            operation.description = worker_text_calendar_day["description"]
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

        elif operation_keys and operation_keys[-1] == "calendar_month":
            worker_text_calendar_month = WORKER_TEXTS["calendar_month"]

            operation.tags = worker_text_calendar_month["tags"]
            operation.summary = worker_text_calendar_month["summary"]
            operation.description = worker_text_calendar_month["description"]

            operation.parameters.append(
                Parameter(
                    "date",
                    IN_PATH,
                    type=TYPE_STRING,
                    format="date",
                    description="Дата в формате ГГГГ-ММ",
                    example="2025-06"
                )
            )
            operation.responses["404"] = OpenApiResponse(worker_text_calendar_month["responses"]["404"], Schema(type=TYPE_OBJECT, properties={"detail": Schema(type=TYPE_STRING, description=worker_text_calendar_month["responses"]["404"])}, example=worker_text_calendar_month["example"]["404"]))
        
        elif operation_keys and operation_keys[-1] == "average_evaluation":
            worker_text_average_evaluation = WORKER_TEXTS["average_evaluation"]

            operation.tags = worker_text_average_evaluation["tags"]
            operation.summary = worker_text_average_evaluation["summary"]
            operation.description = worker_text_average_evaluation["description"]

            operation.parameters.append(
                Parameter(
                    "start_date",
                    IN_PATH,
                    type=TYPE_STRING,
                    format="date",
                    description="Дата в формате ГГГГ-ММ-ДД",
                    example="2025-05-01"
                )
            )
            operation.parameters.append(
                Parameter(
                    "end_date",
                    IN_PATH,
                    type=TYPE_STRING,
                    format="date",
                    description="Дата в формате ГГГГ-ММ-ДД",
                    example="2025-06-01"
                )
            )
            operation.responses["404"] = OpenApiResponse(worker_text_average_evaluation["responses"]["404"], Schema(type=TYPE_OBJECT, properties={"detail": Schema(type=TYPE_STRING, description=worker_text_average_evaluation["responses"]["404"])}, example=worker_text_average_evaluation["example"]["404"]))
        return operation
    

class TokenObtainAutoSchema(SwaggerAutoSchema):
    def get_operation(self, operation_keys=None):
        operation = super().get_operation(operation_keys)
        if operation_keys and operation_keys[-1] == "create":
            if "201" in operation.responses:
                del operation.responses["201"]

            token_obtain_create = TOKEN_OBTAIN_TEXTS["create"]

            operation.tags = token_obtain_create["tags"]
            operation.summary = token_obtain_create["summary"]
            operation.description = token_obtain_create["description"]

            operation.responses["200"] = OpenApiResponse(token_obtain_create["responses"]["200"], Schema(type=TYPE_OBJECT, properties={"access": Schema(type=TYPE_STRING), "refresh": Schema(type=TYPE_STRING)}, example=token_obtain_create["example"]["200"]))
            operation.responses["401"] = OpenApiResponse(token_obtain_create["responses"]["401"], Schema(type=TYPE_OBJECT, properties={"detail": Schema(type=TYPE_STRING)}, example=token_obtain_create["example"]["401"]))
        return operation
    

class TokenBlacklistAutoSchema(SwaggerAutoSchema):
    def get_operation(self, operation_keys=None):
        operation = super().get_operation(operation_keys)
        if operation_keys and operation_keys[-1] == "create":
            if "201" in operation.responses:
                del operation.responses["201"]

            token_blacklist_create = TOKEN_BLACKLIST_TEXTS["create"]

            operation.tags = token_blacklist_create["tags"]
            operation.summary = token_blacklist_create["summary"]
            operation.description = token_blacklist_create["description"]
              
            operation.responses["401"] = OpenApiResponse(token_blacklist_create["responses"]["401"], Schema(type=TYPE_OBJECT, properties={"detail": Schema(type=TYPE_STRING), "code": Schema(type=TYPE_STRING)}, example=token_blacklist_create["example"]["401"]))
        return operation


class TokenRefreshAutoSchema(SwaggerAutoSchema):
    def get_operation(self, operation_keys=None):
        operation = super().get_operation(operation_keys)
        if operation_keys and operation_keys[-1] == "create":
            if "201" in operation.responses:
                del operation.responses["201"]

            token_refresh_create = TOKEN_REFRESH_TEXTS["create"]

            operation.tags = token_refresh_create["tags"]
            operation.summary = token_refresh_create["summary"]
            operation.description = token_refresh_create["description"]
            operation.responses["200"] = OpenApiResponse(token_refresh_create["responses"]["200"], Schema(type=TYPE_OBJECT, properties={"access": Schema(type=TYPE_STRING), "refresh": Schema(type=TYPE_STRING)}, example=token_refresh_create["example"]["200"]))
            operation.responses["401"] = OpenApiResponse(token_refresh_create["responses"]["401"], Schema(type=TYPE_OBJECT, properties={"detail": Schema(type=TYPE_STRING), "code": Schema(type=TYPE_STRING)}, example=token_refresh_create["example"]["401"]))
        return operation
    

class TokenVerifyAutoSchema(SwaggerAutoSchema):
    def get_operation(self, operation_keys=None):
        operation = super().get_operation(operation_keys)
        if operation_keys and operation_keys[-1] == "create":
            if "201" in operation.responses:
                del operation.responses["201"]

            token_verify_create = TOKEN_VERIFY_TEXTS["create"]

            operation.tags = token_verify_create["tags"]
            operation.summary = token_verify_create["summary"]
            operation.description = token_verify_create["description"]
            operation.responses["200"] = OpenApiResponse(token_verify_create["responses"]["200"], Schema(type=TYPE_OBJECT, properties={}, example=token_verify_create["example"]["200"]))
            operation.responses["401"] = OpenApiResponse(token_verify_create["responses"]["401"], Schema(type=TYPE_OBJECT, properties={"detail": Schema(type=TYPE_STRING), "code": Schema(type=TYPE_STRING)}, example=token_verify_create["example"]["401"]))
            operation.responses["400"] = OpenApiResponse(token_verify_create["responses"]["400"], Schema(type=TYPE_OBJECT, properties={"non_field_errors": Schema(type=TYPE_ARRAY, items=Schema(type=TYPE_STRING))}, example=token_verify_create["example"]["400"]))
        return operation
    

class UserAutoSchema(SwaggerAutoSchema):
    def get_operation(self, operation_keys=None):
        operation = super().get_operation(operation_keys)
        print(operation_keys)
        if operation_keys and operation_keys[-1] == "create":
            user_register_create = USER_REGISTER_TEXTS["create"]

            operation.tags = user_register_create["tags"]
            operation.summary = user_register_create["summary"]
            operation.description = user_register_create["description"]
            operation.responses["201"] = OpenApiResponse(user_register_create["responses"]["201"], Schema(type=TYPE_OBJECT, properties={"email": Schema(type=TYPE_STRING), "id": Schema(type=TYPE_INTEGER)}, example=user_register_create["example"]["201"]))     
            operation.responses["400"] = OpenApiResponse(user_register_create["responses"]["400"], Schema(type=TYPE_OBJECT, properties={"name_field": Schema(type=TYPE_ARRAY, items=Schema(type=TYPE_STRING))}, example=user_register_create["example"]["400"]))
        
        elif operation_keys and operation_keys[-2] == "me":
            action = operation_keys[-1]
            if action == "update":
                user_me_update = USER_REGISTER_TEXTS["me_update"]

                operation.tags = user_me_update["tags"]
                operation.summary = user_me_update["summary"]
                operation.description = user_me_update["description"]
                
                operation.responses["400"] = OpenApiResponse(user_me_update["responses"]["400"], Schema(type=TYPE_OBJECT, properties={"name_field": Schema(type=TYPE_ARRAY, items=Schema(type=TYPE_STRING))}, example=user_me_update["example"]["400"]))
            
            elif action == "delete":
                user_me_delete = USER_REGISTER_TEXTS["me_delete"]

                operation.tags = user_me_delete["tags"]
                operation.summary = user_me_delete["summary"]
                operation.description = user_me_delete["description"]
                
                scheme_current_password = Schema(type=TYPE_OBJECT, properties={"current_password": Schema(type=TYPE_STRING)})
                operation.parameters.append(
                    Parameter(
                        "data",
                        IN_BODY,
                        required=True,
                        schema=scheme_current_password
                    )
                )
                operation.responses["204"] = OpenApiResponse(user_me_delete["responses"]["204"])
                operation.responses["401"] = OpenApiResponse(user_me_delete["responses"]["401"], Schema(type=TYPE_OBJECT, properties={"detail": Schema(type=TYPE_STRING), "code": Schema(type=TYPE_STRING)}, example=user_me_delete["example"]["401"])) 
                operation.responses["400"] = OpenApiResponse(user_me_delete["responses"]["400"], Schema(type=TYPE_OBJECT, properties={"name_field": Schema(type=TYPE_ARRAY, items=Schema(type=TYPE_STRING))}, example=user_me_delete["example"]["400"]))
                
        return operation