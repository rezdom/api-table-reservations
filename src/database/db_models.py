from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.database.db import Base, intpk

from datetime import datetime

class TablesOrm(Base):
    __tablename__ = "tables"
    
    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(String(32))
    seats: Mapped[int]
    location: Mapped[str] = mapped_column(String(128))

class ReservationOrm(Base):
    __tablename__ = "reservations"

    id: Mapped[intpk]
    customer_name: Mapped[str] = mapped_column(String(128))
    table_id: Mapped[int] = mapped_column(ForeignKey("tables.id", ondelete="RESTRICT"))
    reservation_time: Mapped[datetime]
    duration_minutes: Mapped[int]