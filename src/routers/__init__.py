from fastapi import APIRouter
from src.routers.table_routers import table_router
from src.routers.reservation_routers import reservation_router

main_router = APIRouter()
routers_list = [table_router, reservation_router]

for item in routers_list:
    main_router.include_router(item)