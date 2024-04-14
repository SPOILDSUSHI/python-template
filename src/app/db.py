
from sqlmodel import SQLModel, create_engine

SQLALCHEMY_DATABASE_URI = "sqlite:///./app.db"

engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)


def init_db() -> None:
    """
    Create the DB if it is new.
    """
    SQLModel.metadata.create_all(engine)
