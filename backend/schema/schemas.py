from pydantic import BaseModel


class BoolResponseSchema(BaseModel):
    result: bool


class ErrorSchema(BaseModel):
    result: bool = False
    error_type: str
    error_message: str
