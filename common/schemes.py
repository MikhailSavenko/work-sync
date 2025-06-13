from drf_yasg.openapi import TYPE_STRING, Response as OpenApiResponse, Schema, TYPE_OBJECT


def get_response_open_api_scheme_with_detail_string_and_example(text: dict, status_code) -> OpenApiResponse:
    response = OpenApiResponse(text["responses"][str(status_code)], 
                               Schema(type=TYPE_OBJECT, 
                                      properties={"detail": Schema(type=TYPE_STRING, 
                                                                   description=text["responses"][str(status_code)])}, 
                                                                   example=text["example"][str(status_code)]))
    return response