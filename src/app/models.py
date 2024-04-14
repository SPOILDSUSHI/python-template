from datetime import datetime, timedelta
from uuid import uuid4

from sqlmodel import Field, SQLModel
from typing_extensions import Annotated

# Shared token properties
class TokenBase(SQLModel):
    endpoint_name: str = Field(unique=True, index=True)
    access_token: str
    refresh_token: str
    expires: datetime
    token_type: str = "Bearer"


# Database model, database table inferred from class name
class Token(TokenBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class TokenUpdate(TokenBase):
    endpoint_name: str | None = None
    access_token: str | None = None
    refresh_token: str | None = None
    expires: datetime | None = None


class TokenCreate(TokenBase):
    pass


class TokenRead(TokenBase):
    id: int

# shared state properties
class StateBase(SQLModel):
    state: Annotated[str, Field(default_factory=lambda: str(uuid4()), index=True)]
    expires: Annotated[
        datetime,
        Field(default_factory=lambda: (datetime.now() + timedelta(seconds=60 * 5))),
    ]


# Database model, database table inferred from class name
class State(StateBase, table=True):
    id: int | None = Field(default=None, primary_key=True, index=True)


class StateRead(StateBase):
    id: int


class StateCreate(StateBase):
    pass

