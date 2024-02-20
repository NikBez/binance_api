from typing import Union

from pydantic import BaseModel


class RequestSchema(BaseModel):
    chat_id: int
    command: str
    params: list[Union[str, int]] | None = None

class ResponseSchema(BaseModel):
    chat_id: int
    text: str


