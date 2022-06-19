from datetime import datetime

from complex_epidemics.model.support_objects.clock import Clock


class TestClock:
    def test_instantiation_without_date(self):

        new_clock = Clock()

        assert isinstance(new_clock, Clock)

    def test_instantiation_with_date(self):

        new_clock = Clock(year=2020, month=3, day=1, hour=0, minute=0)
        year = 2020
        month = 3
        day = 1
        hour = 0
        minute = 0
        test_datetime = datetime(
            year=year, month=month, day=day, hour=hour, minute=minute
        ).isoformat(timespec="minutes")

        assert new_clock.get_datetime() == test_datetime

    def test_method_get_datetime(self):

        new_clock = Clock()
        year = 2000
        month = 1
        day = 1
        hour = 0
        minute = 0
        test_datetime = datetime(
            year=year, month=month, day=day, hour=hour, minute=minute
        ).isoformat(timespec="minutes")

        assert new_clock.get_datetime() == test_datetime

    def test_method_increment_time_in_hours(self):

        new_clock = Clock()
        new_clock.increment_time_in_hours(1)
        year = 2000
        month = 1
        day = 1
        hour = 1
        minute = 0
        test_datetime = datetime(
            year=year, month=month, day=day, hour=hour, minute=minute
        ).isoformat(timespec="minutes")

        assert new_clock.get_datetime() == test_datetime

    def test_method_increment_time_in_days(self):

        new_clock = Clock()
        new_clock.increment_time_in_days(1)
        year = 2000
        month = 1
        day = 2
        hour = 0
        minute = 0
        test_datetime = datetime(
            year=year, month=month, day=day, hour=hour, minute=minute
        ).isoformat(timespec="minutes")

        assert new_clock.get_datetime() == test_datetime
