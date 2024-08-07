from typing_extensions import Any
from pydantic import GetCoreSchemaHandler
from pydantic_core import CoreSchema, core_schema


class ZipCode(str):
    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        return core_schema.no_info_after_validator_function(cls.validate, handler(str))

    @classmethod
    def validate(cls, zipcode: str) -> bool:
        zipcode = zipcode.replace("-", "")

        if len(zipcode) != 8:
            raise ValueError(f"Invalid zipcode: {zipcode}")
