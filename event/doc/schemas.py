from drf_yasg.openapi import Parameter, IN_QUERY, TYPE_STRING, Response as OpenApiResponse, Schema, TYPE_OBJECT, TYPE_STRING, TYPE_ARRAY
from drf_yasg.inspectors.view import SwaggerAutoSchema

from event.doc.texts import ERROR_EXAMPLES, FORBIDDEN_DESCRIPTION, MEETING_TEXTS, VALIDATION_ERROR_DESCRIPTION
from event.serializers import MeetingCreateUpdateSerializer, MeetingGetSerializer


class MeetingAutoSchema(SwaggerAutoSchema):

    VALIDATION_ERROR_SCHEMA = Schema(type=TYPE_OBJECT, properties={
                "non_field_errors": Schema(type=TYPE_ARRAY, items=Schema(type=TYPE_STRING), description=VALIDATION_ERROR_DESCRIPTION)
            }, example=ERROR_EXAMPLES["validation"])

    def get_operation(self, operation_keys=None):
        operation = super().get_operation(operation_keys)

        if operation_keys and operation_keys[-1] == "me":
            operation.summary = MEETING_TEXTS["me"]["summary"]
            operation.description = MEETING_TEXTS["me"]["description"]
            operation.parameters.append(
                Parameter(
                    "done",
                    IN_QUERY,
                    description=MEETING_TEXTS["me"]["done_param"]["description"],
                    type=TYPE_STRING,
                    enum=MEETING_TEXTS["me"]["done_param"]["enum"],
                    default=MEETING_TEXTS["me"]["done_param"]["default"],
                )
            )
            operation.responses = {
                "200": OpenApiResponse(MEETING_TEXTS["me"]["responses"]["200"], Schema(type=TYPE_ARRAY, items=self.serializer_to_schema(MeetingGetSerializer()))),
                "400": OpenApiResponse(MEETING_TEXTS["me"]["responses"]["400"], Schema(type=TYPE_OBJECT, properties={"error": Schema(type=TYPE_STRING)}, example=MEETING_TEXTS["me"]["example"]["400"]))
            }

        elif operation_keys and operation_keys[-1] == "list":
            operation.summary = MEETING_TEXTS["list"]["summary"]
            operation.description = MEETING_TEXTS["list"]["description"]
            operation.responses = {
                "200": OpenApiResponse(MEETING_TEXTS["list"]["responses"]["200"], Schema(type=TYPE_ARRAY, items=self.serializer_to_schema(MeetingGetSerializer()))),
            }
        
        elif operation_keys and operation_keys[-1] == "read":
            operation.summary = MEETING_TEXTS["read"]["summary"]
            operation.description = MEETING_TEXTS["read"]["description"]
            operation.responses = {
                "200": OpenApiResponse(MEETING_TEXTS["read"]["responses"]["200"], self.serializer_to_schema(MeetingGetSerializer())),
                "404": OpenApiResponse(MEETING_TEXTS["read"]["responses"]["404"], Schema(type=TYPE_OBJECT, properties={"detail": Schema(type=TYPE_STRING, description=MEETING_TEXTS["read"]["responses"]["404"])}, example=MEETING_TEXTS["read"]["example"]["404"]))
            }

        elif operation_keys and operation_keys[-1] == "create":
            operation.summary = MEETING_TEXTS["create"]["summary"]
            operation.description = MEETING_TEXTS["create"]["description"]
            operation.request_body = self.get_request_body_schema(MeetingCreateUpdateSerializer())
            
            operation.responses["400"] = OpenApiResponse(MEETING_TEXTS["create"]["responses"]["400"], self.VALIDATION_ERROR_SCHEMA)
        
        elif operation_keys and operation_keys[-1] == "update":
            operation.summary = MEETING_TEXTS["update"]["summary"]
            operation.description = MEETING_TEXTS["update"]["description"]
            operation.request_body = self.get_request_body_schema(MeetingCreateUpdateSerializer())
            
            operation.responses["400"] = OpenApiResponse(MEETING_TEXTS["update"]["responses"]["400"], self.VALIDATION_ERROR_SCHEMA)
        
        elif operation_keys and operation_keys[-1] == "delete":
            operation.summary = MEETING_TEXTS["delete"]["summary"]
            operation.description = MEETING_TEXTS["delete"]["description"]

            operation.responses["403"] = OpenApiResponse(FORBIDDEN_DESCRIPTION, schema=Schema(type=TYPE_OBJECT, properties={"detail": Schema(type=TYPE_STRING, description=MEETING_TEXTS["delete"]["responses"]["403"])}, example=MEETING_TEXTS["delete"]["example"]["403"]))
        return operation