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
