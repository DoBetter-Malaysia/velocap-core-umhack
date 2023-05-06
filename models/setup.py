from sqlalchemy import create_engine
from models.base import Base
from models.startup import Startup
from models.founder import Founder


def setup_models():
    engine = create_engine(
        "postgresql://postgres:mysecretpassword@localhost/main", echo=True
    )

    Base.metadata.create_all(engine)
    return engine
