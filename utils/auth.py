from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from typing import Annotated, Optional
from jwt.exceptions import PyJWTError, ExpiredSignatureError

from db.session import session_dep
from utils.hash import hasher
from utils.db.user import get_user
from utils.jwt_utils import decode_token
from schemas.user import UserSchema
from schemas.exc import (
    IncorrectPasswordException,
    UserNotFoundException,
    UserAuthenticationFailedException,
    UserExpiredTokenException,
)
from schemas.security import TokenData


oauth2_dep = Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl="api/user/login"))]
oauth2_form_dep = Annotated[OAuth2PasswordRequestForm, Depends()]


async def authenticate(
    username: str, password: str, session: session_dep
) -> Optional[UserSchema]:
    user = await get_user(username=username, session=session)
    if user is None:
        raise UserNotFoundException
    if not hasher.verify_password(password, user.password):
        raise IncorrectPasswordException

    return user


async def get_current_client(token: oauth2_dep, session: session_dep) -> UserSchema:
    try:
        payload = decode_token(token)
        if payload:
            data = TokenData(**payload)
            return await get_user(user_id=data.sub, session=session)
        else:
            raise UserAuthenticationFailedException

    except PyJWTError:
        raise UserAuthenticationFailedException
    except ExpiredSignatureError:
        raise UserExpiredTokenException


user_dep = Annotated[UserSchema, Depends(get_current_client)]
