from typing import Optional
from sqlalchemy.orm import Mapped, DeclarativeBase, mapped_column
from models.base import Base


class Founder(Base):
    __tablename__ = "founders"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    linkedin: Mapped[str]
    company_id: Mapped[int]
    description: Mapped[Optional[str]]
    years_of_experience: Mapped[int]
    picture: Mapped[Optional[str]]
    prev_founded: Mapped[int]
