import os
from sqlalchemy import create_engine
from models.base import Base
from models.startup import Startup
from models.founder import Founder
from models.news import News


def setup_models():
    engine = create_engine(
        f"{os.getenv('DATABASE_URL')}{os.getenv('DATABASE_USER')}:{os.getenv('DATABASE_PASSWORD')}@{os.getenv('DATABASE_HOST')}/{os.getenv('DATABASE_DB')}",
        echo=True,
    )

    Base.metadata.create_all(engine)
    return engine
