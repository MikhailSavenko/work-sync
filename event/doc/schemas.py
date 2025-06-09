from drf_yasg.openapi import Parameter, IN_QUERY, TYPE_STRING, Response as OpenApiResponse, Schema, TYPE_OBJECT, TYPE_STRING, TYPE_ARRAY
from drf_yasg.inspectors.view import SwaggerAutoSchema

from event.doc.texts import FORBIDDEN_DESCRIPTION, MEETING_TEXTS, VALIDATION_ERROR_DESCRIPTION
from event.serializers import MeetingCreateUpdateSerializer, MeetingGetSerializer


class MeetingAutoSchema(SwaggerAutoSchema):

    def get_operation(self, operation_keys=None):
        operation = super().get_operation(operation_keys)

        if operation_keys and operation_keys[-1] == "me":
            meeting_text_me = MEETING_TEXTS["me"]

            operation.tags = meeting_text_me["tags"]
            operation.summary = meeting_text_me["summary"]
            operation.description = meeting_text_me["description"]
            operation.parameters.append(
                Parameter(
                    "done",
                    IN_QUERY,
                    description=meeting_text_me["done_param"]["description"],
                    type=TYPE_STRING,
                    enum=meeting_text_me["done_param"]["enum"],
                    default=meeting_text_me["done_param"]["default"],
                )
            )
            operation.responses["400"] = OpenApiResponse(meeting_text_me["responses"]["400"], Schema(type=TYPE_OBJECT, properties={"detail": Schema(type=TYPE_STRING)}, example=meeting_text_me["example"]["400"]))
    
        elif operation_keys and operation_keys[-1] == "list":
            meeting_text_list = MEETING_TEXTS["list"]

            operation.tags = meeting_text_list["tags"]
            operation.summary = meeting_text_list["summary"]
            operation.description = meeting_text_list["description"]
        
        elif operation_keys and operation_keys[-1] == "read":
            meeting_text_read = MEETING_TEXTS["read"]

            operation.tags = meeting_text_read["tags"]
            operation.summary = meeting_text_read["summary"]
            operation.description = meeting_text_read["description"]

            operation.responses["404"] = OpenApiResponse(meeting_text_read["responses"]["404"], Schema(type=TYPE_OBJECT, properties={"detail": Schema(type=TYPE_STRING, description=meeting_text_read["responses"]["404"])}, example=meeting_text_read["example"]["404"]))
            
        elif operation_keys and operation_keys[-1] == "create":
            meeting_text_create = MEETING_TEXTS["create"]

            operation.tags = meeting_text_create["tags"]
            operation.summary = meeting_text_create["summary"]
            operation.description = meeting_text_create["description"]
            
            operation.responses["400"] = OpenApiResponse(meeting_text_create["responses"]["400"], Schema(type=TYPE_OBJECT, properties={"name_field": Schema(type=TYPE_ARRAY, items=Schema(type=TYPE_STRING))}, example=meeting_text_create["example"]["400"]))
            operation.responses["409"] = OpenApiResponse(meeting_text_create["responses"]["409"], Schema(type=TYPE_OBJECT, properties={"detail": Schema(type=TYPE_STRING, description=meeting_text_create["responses"]["409"])}, example=meeting_text_create["example"]["409"]))
        
        elif operation_keys and operation_keys[-1] == "update":
            operation.summary = MEETING_TEXTS["update"]["summary"]
            operation.description = MEETING_TEXTS["update"]["description"]
            operation.request_body = self.get_request_body_schema(MeetingCreateUpdateSerializer())
            
            # operation.responses["400"] = OpenApiResponse(MEETING_TEXTS["update"]["responses"]["400"], self.VALIDATION_ERROR_SCHEMA)
        
        elif operation_keys and operation_keys[-1] == "delete":
            operation.summary = MEETING_TEXTS["delete"]["summary"]
            operation.description = MEETING_TEXTS["delete"]["description"]

            operation.responses["403"] = OpenApiResponse(FORBIDDEN_DESCRIPTION, schema=Schema(type=TYPE_OBJECT, properties={"detail": Schema(type=TYPE_STRING, description=MEETING_TEXTS["delete"]["responses"]["403"])}, example=MEETING_TEXTS["delete"]["example"]["403"]))
        return operation