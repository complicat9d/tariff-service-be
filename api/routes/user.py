from fastapi import APIRouter, status
from sqlalchemy.exc import IntegrityError

from db.session import session_dep
from schemas.user import UserCreateSchema
from schemas.security import TokenResponse
from schemas.exc import UserAlreadyExistsException
from utils.db.user import create_user
from utils.auth import authenticate, oauth2_form_dep
from utils.jwt_utils import create_jwt_access_token
from utils.log import logger

user_router = APIRouter(tags=["User"])


@user_router.post(
    path="/create", status_code=status.HTTP_201_CREATED, response_model=TokenResponse
)
async def _create_user(request: UserCreateSchema, session: session_dep):
    try:
        client_id = await create_user(request, session)
    except IntegrityError:
        raise UserAlreadyExistsException
    logger.info(
        f"Client with username {request.username} has been successfully registered"
    )
    return TokenResponse(access_token=create_jwt_access_token(client_id))


@user_router.post("/login", response_model=TokenResponse, include_in_schema=False)
async def _login(form: oauth2_form_dep, session: session_dep):
    user = await authenticate(
        username=form.username, password=form.password, session=session
    )
    return TokenResponse(access_token=create_jwt_access_token(user.id))
