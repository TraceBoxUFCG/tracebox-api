from app.common.schemas.validator_types import Validator


class ZipCode(Validator):
    @classmethod
    def validate(cls, zipcode: str) -> bool:
        zipcode = zipcode.replace("-", "")

        if len(zipcode) != 8:
            raise ValueError(f"Invalid zipcode: {zipcode}")
