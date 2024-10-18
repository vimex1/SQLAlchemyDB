import datetime
from typing import Optional, Annotated
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, text, func
from sqlalchemy.orm import Mapped, mapped_column
from database import Base, str_256
import enum


intpk = Annotated[int, mapped_column(primary_key=True)]

created_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]

updated_at = Annotated[datetime.datetime, mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.datetime.utcnow,
    )]

class WorkersOrm(Base):
    """
    Таблица workers
    """
    __tablename__ = "workers"

    id: Mapped[intpk]
    username: Mapped[str]


class Workload(enum.Enum):
    """
    Класс-тип рабочего времени
    """
    parttime = "parttime"   # частичная занятость
    fulltime = "fulltime"   # полная занятость

class ResumesOrm(Base):
    """
    Таблица resumes
    """
    __tablename__ = "resumes"

    # столбцы
    id: Mapped[intpk]  # id резюме, primary key
    title: Mapped[str]  # заголовок резюме
    compensation: Mapped[int | None]  # зарплата, может быть None
    workload: Mapped[Workload]  # тип занятости
    worker_id: Mapped[int] = mapped_column(             # id работника, для которого это резюме
        ForeignKey("workers.id", ondelete="CASCADE")    # foreign key, связанный с workers.id
    )
    created_at: Mapped[created_at]  # дата создания
    updated_at: Mapped[updated_at]  # дата обновления













metadata_obj = MetaData()

workers_table = Table(
    "workers",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("username", String),
)