from fastapi import HTTPException
from starlette import status


class UserExceptions:
    NotFound = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail='User not found.'
    )

    PhoneAlreadyUsed = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail='This phone number already in used.'
    )

    TelegramAlreadyUsed = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail='This telegram id already in used.'
    )

    NameInvalid = HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail='Incorrect string.'
    )

    PhoneInvalid = HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail='Phone number incorrect.'
    )
