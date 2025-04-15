from fastapi import APIRouter, HTTPException
from typing import List

from src.database.orm import AsyncOrmTables
from src.schemas.table_schemas import InsertTableSchema, ResponseTableSchema

table_router = APIRouter()

@table_router.get("/tables/", tags=["Tables"], summary="get all tables", response_model=List[ResponseTableSchema])
async def get_tables():
    result = await AsyncOrmTables.get_tables()
    if result: return result
    raise HTTPException(status_code=404, detail="No tables found")

@table_router.post("/tables/", tags=["Tables"], summary="create table", response_model=ResponseTableSchema)
async def post_table(new_table: InsertTableSchema):
    result = await AsyncOrmTables.insert_table(
        new_table.name,
        new_table.seats,
        new_table.location
    )
    if result: return result
    raise HTTPException(status_code=500, detail="Internal Server Error")

@table_router.delete("/tables/{id}", tags=["Tables"], summary="delete table", response_model=ResponseTableSchema)
async def delete_table(del_id: int):
    try:
        result = await AsyncOrmTables.delete_table(del_id)
        if result: return result
    except HTTPException as e:
        raise e