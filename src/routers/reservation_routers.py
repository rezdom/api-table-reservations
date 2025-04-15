from fastapi import APIRouter, HTTPException
from typing import List

from src.database.orm import AsyncOrmReservation
from src.schemas.reservation_schemas import InsertReservationSchema, ResponseReservationSchema

reservation_router = APIRouter()

@reservation_router.get("/reservations/", tags=["Reservation"], summary="get all reservations", response_model=List[ResponseReservationSchema])
async def get_reservations():
    result = await AsyncOrmReservation.get_reservations()
    if result: return result
    raise HTTPException(status_code=404, detail="reservations not found")

@reservation_router.post("/reservations/", tags=["Reservation"], summary="create reservation", response_model=ResponseReservationSchema)
async def post_reservation(new_reser: InsertReservationSchema):
    result = await AsyncOrmReservation.insert_reservation(
        new_reser.customer_name,
        new_reser.table_id,
        new_reser.reservation_time,
        new_reser.duration_minutes
    )
    if result: return result
    raise HTTPException(status_code=400, detail="overlapping time")

@reservation_router.delete("/reservations/{id}", tags=["Reservation"], summary="delete reservation", response_model=ResponseReservationSchema)
async def delete_reservation(del_id: int):
    result = await AsyncOrmReservation.delete_reservation(del_id)
    if result: return result
    raise HTTPException(status_code=404, detail="No tables found to delete")