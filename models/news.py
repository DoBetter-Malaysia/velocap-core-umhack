from dataclasses import dataclass
from typing import Optional
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import Mapped, DeclarativeBase, mapped_column, relationship
from models.base import Base
from sqlalchemy.types import Date


@dataclass
class News(Base):
    __tablename__ = "news"

    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(Integer, ForeignKey("startups.id"))
    headline: Mapped[str]
    source: Mapped[str]
    date_posted: Mapped[Date] = Column(Date, nullable=True)
    sentiment_result: Mapped[int]

    company = relationship("Startup")
