# -*- coding: utf-8 -*-
"""Model clock module.
"""

import logging
from datetime import datetime, timedelta

LOG = logging.getLogger(__name__)


class Clock:
    """Model clock class."""

    def __init__(
        self,
        year: int = 2000,
        month: int = 1,
        day: int = 1,
        hour: int = 0,
        minute: int = 0,
    ) -> None:
        """Model Clock class.

        Parameters
        ----------
        year : int, optional
            year, by default 1997
        month : int, optional
            month (1 to 12), by default 1
        day : int, optional
            day (1 to 31), by default 1
        hour : int, optional
            hour (0 to 23), by default 0
        minute : int, optional
            minute (0 to 59), by default 0
        """
        try:
            self._datetime = datetime(year, month, day, hour, minute)
        except Exception as err:
            LOG.exception(f"Failed to set datetime. Exception: {err}")
            raise

    def get_datetime_formated(self) -> str:
        """Return a string with formatted datetime to minutes.

        Returns
        -------
        str
            Formatted datetime to YYYY-MM-DDTHH-mm
        """
        return self._datetime.isoformat(timespec="minutes")

    def get_datetime(self) -> datetime:
        """Return a datetime object.

        Returns
        -------
        datetime
            Python datetime object.
        """
        return self._datetime

    def increment_time_in_hours(self, hours: int) -> str:
        """Advance Clock to a specified number of hours.

        Parameters
        ----------
        hours : int
            Number of hours to advance.
        """
        self._datetime += timedelta(hours=hours)
        return self._datetime.isoformat(timespec="minutes")

    def increment_time_in_days(self, days: int) -> str:
        """Advance Clock to a specified number of days.

        Parameters
        ----------
        days : int
            Number of days to advance.
        """
        self._datetime += timedelta(days=days)
        return self._datetime.isoformat(timespec="minutes")
