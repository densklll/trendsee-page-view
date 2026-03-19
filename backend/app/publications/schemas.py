from datetime import datetime

from pydantic import BaseModel, Field, model_validator


class PublicationCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)
    text: str = Field(..., min_length=1, max_length=50000)


class PublicationUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=500)
    text: str | None = Field(None, min_length=1, max_length=50000)

    @model_validator(mode="after")
    def at_least_one_field(self):
        if self.title is None and self.text is None:
            raise ValueError("At least one of 'title' or 'text' must be provided")
        return self


class PublicationResponse(BaseModel):
    id: int
    user_id: int
    title: str
    text: str
    cover_asset: str | None = None
    created_at: datetime
    updated_at: datetime
    source: str


class PaginatedPublicationsResponse(BaseModel):
    items: list[PublicationResponse]
    total: int
    limit: int
    offset: int
