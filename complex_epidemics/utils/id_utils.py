import uuid
from typing import Any

from complex_epidemics.utils.exceptions import InvalidOptionError


class IDUtils:
    @staticmethod
    def generate_id(id_type: int = 4, fmt: str = "integer") -> Any:
        """Unique ID generator.

        Returns
        -------
        int
            Unique ID of type integer (numeric).
        """
        match id_type:
            case 1:
                match fmt:
                    case "alphanumeric":
                        return uuid.uuid1()
                    case "integer":
                        return uuid.uuid1().int
                    case "hexadecimal":
                        return uuid.uuid1().hex
                    case _:
                        raise InvalidOptionError(f'Format "{fmt}" is invalid.')
            case 4:
                match fmt:
                    case "alphanumeric":
                        return uuid.uuid4()
                    case "integer":
                        return uuid.uuid4().int
                    case "hexadecimal":
                        return uuid.uuid4().hex
                    case _:
                        raise InvalidOptionError(f'Format "{fmt}" is invalid.')
            case _:
                raise InvalidOptionError(f'Type "{id_type}" is invalid.')
