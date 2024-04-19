from fastapi import HTTPException, status


class AuthenticationExceptions:
    RefreshNotFound = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail='Refresh token not found.'
    )

    RefreshExpires = HTTPException(
        status_code=status.HTTP_410_GONE, detail='Refresh token was expired.'
    )

    AccessNotFound = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail='Access token not found.'
    )

    AccessExpires = HTTPException(
        status_code=status.HTTP_410_GONE, detail='Access token was expired.'
    )

    ConflictPhone = HTTPException(
        status_code=status.HTTP_409_CONFLICT, detail='Phone number already used another user.'
    )

    ConflictTelegram = HTTPException(
        status_code=status.HTTP_409_CONFLICT, detail='Telegram already used another user.'
    )

    InvalidCredentials = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail='Invalid credentials.'
    )

    InvalidRole = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="The user role doesn't allow you to get this."
    )
    