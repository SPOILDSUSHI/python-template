from collections.abc import Generator
from contextlib import asynccontextmanager
from datetime import datetime, timedelta
from typing import Annotated

import httpx
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from sqlmodel import Session, select

from app import crud, models
from app.db import engine, init_db


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]


@asynccontextmanager
async def lifespan(app: FastAPI) -> Generator[None, None, None]:
    init_db()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def index() -> dict[str, str]:
    """Index endpoint

    Returns:
        RedirectResponse: Redirects to the redoc endpoint.

    """
    return {"hello": "World"}


@app.get("/login", response_class=RedirectResponse)
async def login(*, session: SessionDep) -> RedirectResponse:
    """Login endpoint

    This endpoint will login via OAuth 2.0 Authorization flow.  First,
    it checks for existing tokens.  If none it will purge expired states
    and then redirect to the authorize uri.  For expired tokens it performs a
    refresh.  For valid tokens it will do nothing.

    Args:
        session (SessionDep): The DB session is an injected dependency.

    Returns:
        RedirectResponse: Redirects depending on the state of the token.

    Todo:
        *make dynamic to accept different downstream logins
    """

    statement = select(models.Token).where(models.Token.endpoint_name == "test")
    result = session.exec(statement).first()
    if result is None:

        crud.purge_invalid_states(session=session)
        state = crud.create_state(session=session)

        auth_uri = f"test_uri+redirect_uri=test_redirect+state={state.state}"

        return RedirectResponse(url=auth_uri)

    elif result.expires <= datetime.now():
        auth = httpx.BasicAuth(username="client_id", password="client_secret")  # nosec
        post_data = {
            "grant_type": "refresh_token",
            "refresh_token": result.refresh_token,
        }
        response = httpx.post("third party uri", data=post_data, auth=auth)
        response_json = response.json()
        print(response_json)

        try:
            crud.update_token(
                session=session,
                endpoint_name="test",
                token_in=models.TokenUpdate(
                    access_token=response_json["access_token"],
                    refresh_token=response_json["refresh_token"],
                    expires=(
                        datetime.now() + timedelta(seconds=response_json["expires_in"])
                    ),
                ),
            )
        except KeyError as err:
            raise HTTPException(status_code=400, detail=response_json) from err

        return RedirectResponse("/?success=Refreshed_token")

    else:
        return RedirectResponse("/?nothing=already_logged_in")


@app.get("/auth_callback")
async def auth_callback(*, session: SessionDep, code: str, state: str):
    """
    Logic:  Check the redirect for a valid state (exists in DB and is
    not expired).
    Send the token request.
    Parse the json response and save token to DB.
    """
    statement = select(models.State).where(models.State.state == state)
    is_valid_state = session.exec(statement).first()
    if not is_valid_state:
        raise HTTPException(status_code=403, detail="Invalid state")
    if is_valid_state.expires <= datetime.now():
        raise HTTPException(status_code=403, detail="Expired state")

    auth = httpx.BasicAuth(username="client_id", password="client_secret")  # nosec
    post_data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": "test_redirect_uri",
    }
    response = httpx.post("third party uri", data=post_data, auth=auth)
    response_json = response.json()

    try:
        crud.create_token(
            session=session,
            token=models.TokenCreate(
                endpoint_name="test",
                token_type=response_json["token_type"],
                access_token=response_json["access_token"],
                refresh_token=response_json["refresh_token"],
                scope=response_json["scope"],
                expires=(
                    datetime.now() + timedelta(seconds=response_json["expires_in"])
                ),
            ),
        )
    except KeyError as err:
        raise HTTPException(status_code=400, detail=response_json) from err

    return {"success": "Logged in"}
