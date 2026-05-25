from pydantic import BaseModel


class DeleteResponse(BaseModel):
    deleted: bool