# -*- coding: utf-8 -*-
"""Complex Epidemics Simulator custom exceptions module.
"""


class InvalidTypeError(TypeError):
    """Invalid Type Error exception.

    Raised when an invalid or non-implemented enumeration type is used.
    """

    pass


class InvalidOptionError(ValueError):
    """Invalid Option Error exception.

    Raised when an invalid or non-implemented option is used.
    """

    pass


class MissingDataError(ValueError):
    """Missing Data Error exception.

    Raised when required data is missing.
    """

    pass
