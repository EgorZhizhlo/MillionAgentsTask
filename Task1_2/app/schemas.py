from pydantic import BaseModel, Field


class SUrl(BaseModel):
    url: str
