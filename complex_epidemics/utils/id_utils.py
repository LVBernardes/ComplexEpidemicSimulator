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
        if id_type == 1:
            if fmt == "alphanumeric":
                return uuid.uuid1()
            elif fmt == "integer":
                return uuid.uuid1().int
            elif fmt == "hexadecimal":
                return uuid.uuid1().hex
            else:
                raise InvalidOptionError(f'Format "{fmt}" is invalid.')
        elif id_type == 4:
            if fmt == "alphanumeric":
                return uuid.uuid4()
            elif fmt == "integer":
                return uuid.uuid4().int
            elif fmt == "hexadecimal":
                return uuid.uuid4().hex
            else:
                raise InvalidOptionError(f'Format "{fmt}" is invalid.')
        else:
            raise InvalidOptionError(f'Type "{id_type}" is invalid.')
