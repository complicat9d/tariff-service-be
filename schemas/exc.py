from fastapi import HTTPException, status


TariffNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Tariff not found"
)

TariffAlreadyExistsException = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN, detail="Tariff already exists"
)

InvalidJSONException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid json format"
)

UserNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
)

UserAuthenticationFailedException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="User authentication failed"
)

IncorrectPasswordException = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Incorrect password for the given username",
)

UserAlreadyExistsException = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="User with the given username already exists",
)

UserExpiredTokenException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="User token has been expired, try logging in again",
)
