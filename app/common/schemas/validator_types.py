from typing import Any, Dict
from pydantic_core import core_schema


JsonSchemaValue = Dict[str, Any]


class Validator:
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source,
    ) -> core_schema.CoreSchema:
        return core_schema.with_info_after_validator_function(
            function=cls._validate, schema=core_schema.str_schema()
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: core_schema.CoreSchema, handler
    ) -> JsonSchemaValue:
        field_schema = handler(core_schema)
        field_schema.update(type="string", format=cls.format)
        return field_schema

    @classmethod
    def _validate(cls, __input_value: str, _: core_schema.ValidationInfo) -> str:
        return cls.validate(__input_value)
