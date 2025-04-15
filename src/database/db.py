from sqlalchemy import Integer
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, mapped_column

from typing import Annotated

from src.database.config import settings

async_engine = create_async_engine(
    url = settings.asybc_get_db_url,
    echo = False,
    pool_size=10,
    max_overflow=20,
)
async_session_fuctory = async_sessionmaker(async_engine)

intpk = Annotated[int, mapped_column(primary_key=True)]

class Base(DeclarativeBase):
    type_annotation_map = {
        intpk: Integer(),
    }