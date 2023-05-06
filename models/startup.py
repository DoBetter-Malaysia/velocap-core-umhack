from dataclasses import dataclass
from typing import Optional, List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Column
from sqlalchemy.types import Date
from models.base import Base
from models.founder import Founder


@dataclass
class Startup(Base):
    __tablename__ = "startups"

    id: Mapped[int] = mapped_column(primary_key=True)
    permalink: Mapped[str]
    name: Mapped[str]
    homepage_url: Mapped[str]
    description: Mapped[Optional[str]]
    picture: Mapped[str]
    category_list: Mapped[str]
    market: Mapped[str]
    funding_total_usd: Mapped[Optional[int]]
    status: Mapped[str]
    country_code: Mapped[str]
    funding_rounds: Mapped[int]
    founded_at: Mapped[Date] = Column(Date)
    first_funding_at: Mapped[Date] = Column(Date, nullable=True)
    last_funding_at: Mapped[Date] = Column(Date, nullable=True)
    last_engagement_at: Mapped[Date] = Column(Date, nullable=True)
    seed: Mapped[int]
    venture: Mapped[int]
    equity_crowdfunding: Mapped[int]
    undisclosed: Mapped[int]
    convertible_note: Mapped[int]
    debt_financing: Mapped[int]
    angel: Mapped[int]
    grant: Mapped[int]
    private_equity: Mapped[int]
    post_ipo_equity: Mapped[int]
    post_ipo_debt: Mapped[int]
    secondary_market: Mapped[int]
    product_crowdfunding: Mapped[int]
    round_A: Mapped[int]
    round_B: Mapped[int]
    round_C: Mapped[int]
    round_D: Mapped[int]
    round_E: Mapped[int]
    round_F: Mapped[int]
    round_G: Mapped[int]
    round_H: Mapped[int]
    market_size: Mapped[str]

    founders: Mapped[List["Founder"]] = relationship()
    
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}
