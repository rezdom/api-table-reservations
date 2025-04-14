from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import async_session_fuctory
from src.database.db_models import TablesOrm, ReservationOrm

from datetime import datetime, timedelta

class AsyncOrmTables:
    @staticmethod
    async def get_tables():
        async with async_session_fuctory() as session:
            query = select(TablesOrm)
            result = await session.execute(query)
            tables = result.scalars().all()
            return tables
    
    @staticmethod
    async def insert_table(new_name: str, new_seats: int, new_location: str):
        async with async_session_fuctory() as session:
            new_table = TablesOrm(name=new_name, seats=new_seats, location=new_location)
            session.add(new_table)
            await session.commit()
            await session.refresh(new_table)
            return new_table
    
    @staticmethod
    async def delete_table(id: int):
        del_item = None
        async with async_session_fuctory() as session:
            table = await session.get(TablesOrm, id)
            if table:
                del_item = table
                await session.delete(table)
                await session.commit()
        return del_item



class AsyncOrmReservation:
    @staticmethod
    async def __search_table(session: AsyncSession, check_id: int):
        query = select(TablesOrm).filter(TablesOrm.id == check_id)
        result = await session.execute(query)
        return result.scalars().first()
    
    @staticmethod
    async def __search_overlap(session: AsyncSession, start_time: datetime, end_time: datetime, table_id: int):
        query = select(ReservationOrm).filter(
            ReservationOrm.id == table_id,
            and_(
                ReservationOrm.reservation_time < end_time,
                ReservationOrm.reservation_time + timedelta(minutes=ReservationOrm.duration_minutes) > start_time
            )
        )
        result = await session.execute(query)
        return result.scalars().first()

    @staticmethod
    async def get_reservations():
        async with async_session_fuctory() as session:
            query = select(ReservationOrm)
            result = await session.execute(query)
            reservations = result.scalars().all()
            return reservations
    
    @staticmethod
    async def insert_reservation(new_customer_name: str, new_table_id: int, new_reservation_time: datetime, new_duration_minutes: int):
        async with async_session_fuctory() as session:
            result = None
            table = await AsyncOrmReservation.__search_table(session, new_table_id)
            if table:
                new_reservation_end_time = new_reservation_time + timedelta(minutes=new_duration_minutes)
                overlapping = await AsyncOrmReservation.__search_overlap(session, new_reservation_time, new_reservation_end_time, new_table_id)
                if not overlapping:
                    new_reservation = ReservationOrm(
                        customer_name = new_customer_name,
                        table_id = new_table_id,
                        reservation_time = new_reservation_time,
                        duration_minutes = new_duration_minutes,
                    )
                    session.add(new_reservation)
                    await session.commit()
                    await session.refresh(new_reservation)
                    result = new_reservation
            return result

    @staticmethod
    async def delete_reservation(id: int):
        del_item = None
        async with async_session_fuctory() as session:
            reservation = await session.get(ReservationOrm, id)
            if reservation:
                del_item = reservation
                await session.delete(reservation)
                await session.commit()
        return del_item

# from fastapi import APIRouter, Depends
# from typing import List

# router = APIRouter()

# @router.get("/tables", response_model=List[TableSchema])
# async def get_all_tables():
#     async with async_session_fuctory() as session:
#         result = await session.execute(select(TablesOrm))
#         tables = result.scalars().all()
#         return tables
