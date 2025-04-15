from pydantic import BaseModel, Field, ConfigDict

class InsertTableSchema(BaseModel):
    name: str = Field(max_length=32)
    seats: int = Field(ge=0, le=20)
    location: str = Field(max_length=128)

    model_config = ConfigDict(extra="forbid")

class ResponseTableSchema(InsertTableSchema):
    id: int

    class Config:
        orm_mode = True