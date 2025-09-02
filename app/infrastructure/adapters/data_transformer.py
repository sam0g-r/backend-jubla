from datetime import date, datetime
from decimal import Decimal
import json
from typing import Any, Dict, Union

class DataTransformer:
    @staticmethod
    def to_json_safe(obj: Any) -> Union[Dict, list, str, int, float, bool, None]:
        """Convierte cualquier objeto en un tipo JSON-safe."""
        def _default(o: Any) -> Union[str, float]:
            if isinstance(o, (datetime, date)):
                return o.isoformat()
            if isinstance(o, Decimal):
                return float(o)
            return str(o)
        
        return json.loads(json.dumps(obj, default=_default))

    @staticmethod
    def prepare_prisma_filters(filters: Dict) -> Dict:
        """Prepara filtros para consultas Prisma."""
        if not filters:
            return {}
        
        return {
            key: value
            for key, value in filters.items()
            if value is not None
        }

    @staticmethod
    def prepare_enum_value(field_value: Any) -> Any:
        """Extrae el valor de un enum si es necesario."""
        return field_value.value if hasattr(field_value, "value") else field_value
