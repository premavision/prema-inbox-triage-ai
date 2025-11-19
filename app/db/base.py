"""Database metadata helpers."""

from sqlmodel import SQLModel


class BaseModel(SQLModel):
    """Base SQLModel with shared config."""

    class Config:
        arbitrary_types_allowed = True
        orm_mode = True
