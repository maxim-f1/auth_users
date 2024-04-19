import re

from pydantic import StringConstraints, SecretStr, BaseModel, ConfigDict

PhoneStr = StringConstraints(min_length=4, max_length=15, pattern=re.compile(r'^\d+$'))


class CustomSecretStr(SecretStr, str):
    pass


class AbstractDTO(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True
    )
