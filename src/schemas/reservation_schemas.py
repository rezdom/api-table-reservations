from pydantic import BaseModel, Field, field_validator
from datetime import datetime

class InsertReservationSchema(BaseModel):
    customer_name: str = Field(max_length=128)
    table_id: int = Field(ge=1)
    reservation_time: datetime
    duration_minutes: int = Field(ge=30, le=720)

    
class ResponseReservationSchema(InsertReservationSchema):
    id: int

    class Config:
        orm_mode = True