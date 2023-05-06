from dataclasses import dataclass
from typing import Optional
from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, DeclarativeBase, mapped_column, relationship
from models.base import Base

@dataclass
class Founder(Base):
    __tablename__ = "founders"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    linkedin: Mapped[str]
    company_id: Mapped[int] = mapped_column(Integer, ForeignKey("startups.id"))
    description: Mapped[Optional[str]]
    years_of_experience: Mapped[int]
    picture: Mapped[Optional[str]]
    prev_founded: Mapped[int]
    gender: Mapped[str]
    
    startup = relationship("Startup")
