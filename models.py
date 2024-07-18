from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, DateTime, text
import enum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.inspection import inspect
from typing import Annotated
from datetime import datetime

metadata = MetaData()

workers_table = Table(
    'workers',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(50)),
)

str_256 = Annotated[str, mapped_column(String(256), nullable=True)]


class Base(DeclarativeBase):

    def __repr__(self):
        # Получаем имя класса
        class_name = self.__class__.__name__

        # Получаем все атрибуты модели
        mapper = inspect(self.__class__)
        attributes = []

        for column in mapper.columns:
            value = getattr(self, column.key)
            # Форматируем строковые значения в кавычках
            if isinstance(value, str):
                value = f"'{value}'"
            attributes.append(f"{column.key}={value}")

        # Собираем строку представления
        return f"{class_name}({', '.join(attributes)})"


class Workload(enum.Enum):
    fulltime = "fulltime"
    parttime = "parttime"


class Worker(Base):
    __tablename__ = 'workers'

    @classmethod
    def get_mapper(cls):
        return inspect(cls)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str]
    descr: Mapped[str_256]
    workload: Mapped[Workload] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("timezone('UTC', CURRENT_TIMESTAMP)")
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("timezone('UTC', CURRENT_TIMESTAMP)")
    )
    resumes: Mapped[list["Resume"]] = relationship(back_populates="worker")
    # primaryjoin - возможность join с условием
    resumes_parttime: Mapped[list["Resume"]] = relationship(
        back_populates="worker",
        primaryjoin="and_(Resume.worker_id==Worker.id, Resume.workload=='parttime')",
        order_by="Resume.id.desc()"
    )

    def __str__(self):
        return f"id: {self.id}, name: {self.name}"

    # def __repr__(self):
    #     return f"id: {self.id}, name: {self.name}"


class Resume(Base):

    __tablename__ = 'resume'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str]
    compensation: Mapped[int]
    workload: Mapped[Workload]
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("timezone('UTC', CURRENT_TIMESTAMP)")
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("timezone('UTC', CURRENT_TIMESTAMP)")
    )
    worker_id: Mapped[int] = mapped_column(ForeignKey("workers.id", ondelete="CASCADE"))
    worker: Mapped["Worker"] = relationship(back_populates="resumes")
    # backref - устаревший вариант, который заменяет поле модели с relationship и back_populates

# class Vacancy(Base):
#     id: Mapped[int] = mapped_column(primary_key=True)
