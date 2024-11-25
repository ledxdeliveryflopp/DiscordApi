

class OpenApiErrors:
    errors: dict = {404: {"description": "User with this username, dont exist",
                          "content": {"application/json": {"example":  {"detail": "User dont exist."}}}},
                    400: {"description": "Error when the database saved an object",
                          "content": {"application/json": {"example": {"detail": "save error."}}}}}


open_api_errors = OpenApiErrors()
