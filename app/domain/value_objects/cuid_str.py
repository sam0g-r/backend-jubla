import re
from typing import Any
from pydantic import GetCoreSchemaHandler
from pydantic_core import CoreSchema, core_schema

cuid_pattern = re.compile(r"^c[^\s-]{8,}$")

class CuidStr(str):
    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        return core_schema.no_info_after_validator_function(
            cls.validate,
            core_schema.str_schema(),
        )

    @classmethod
    def validate(cls, v: Any) -> str:
        if not isinstance(v, str):
            raise TypeError("Debe ser un string")
        if not cuid_pattern.match(v):
            raise ValueError("Debe ser un CUID válido")
        return v

    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: CoreSchema, handler
    ):
        json_schema = handler(core_schema)
        json_schema.update(
            type="string",
            format="cuid",
            example="ckl7d1e8p000001l6p1s4d9m1",
            description="Identificador único en formato CUID"
        )
        return json_schema