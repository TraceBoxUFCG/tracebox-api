from app.common.schemas.validator_types import Validator


class ZipCode(Validator):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, zipcode: str) -> bool:
        zipcode = zipcode.replace("-", "")

        if len(zipcode) != 8:
            raise ValueError(f"Invalid zipcode: {zipcode}")
