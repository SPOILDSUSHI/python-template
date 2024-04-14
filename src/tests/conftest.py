import os
from collections.abc import Generator

import pytest

from fastapi.testclient import TestClient

from sqlmodel import Session, SQLModel, create_engine, delete
from sqlmodel.pool import StaticPool

from app.main import app, get_db
from app.models import State, Token


connect_args = {"check_same_thread": False}
test_sqlalchemy_database_uri = "sqlite://"
engine = create_engine(
    test_sqlalchemy_database_uri,
    connect_args=connect_args,
    poolclass=StaticPool,
    echo=True,
)
SQLModel.metadata.create_all(engine)


@pytest.fixture(scope="session", autouse=True)
def db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
        statement = delete(State)
        session.exec(statement)
        statement = delete(Token)
        session.exec(statement)
        session.commit()


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    """
    I had to get kludgey with the fixture.  It is not callable when imported but does
    meet pytest standards without inserting as param.  The other issue would be
    testing in the live DB.
    """

    def _db() -> Generator[Session, None, None]:
        with Session(engine) as session:
            yield session
            statement = delete(State)
            session.exec(statement)
            statement = delete(Token)
            session.exec(statement)
            session.commit()

    app.dependency_overrides[get_db] = _db
    with TestClient(app=app, follow_redirects=False) as c:
        yield c


# @pytest.fixture
# def mock_token_api() -> Generator[MockRouter, None, None]:
#     with respx.mock(base_url=third_party_url, assert_all_called=False) as respx_mock:
#         yield respx_mock
