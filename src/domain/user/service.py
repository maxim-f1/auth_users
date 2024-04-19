from src.database.postgres.depends import get_session
from src.domain.authentication.exception import AuthenticationExceptions
from src.domain.authentication.service import Hasher
from src.domain.user.dal import UserDAO
from src.domain.user.dto import UserCreateDTO, UserGetDTO, RoleEnum


async def user_create(session: get_session, user_data: UserCreateDTO) -> UserGetDTO:
    conflict_by_phone_user = await UserDAO(session).get_by_phone(phone=user_data.phone)
    if conflict_by_phone_user is not None:
        raise AuthenticationExceptions.ConflictPhone

    user_data.password = Hasher.get_password_hash(user_data.password)
    data_to_insert = UserCreateDTO.model_validate(user_data)
    new_user = await UserDAO(session).create(data_to_insert)
    return new_user
