from complex_epidemics.agents.support_objects.time_counter import TimeCounter


class TestTimeCounter:
    def test_instantiation(self):

        new_time_counter = TimeCounter()

        assert isinstance(new_time_counter, TimeCounter)

    def test_method_increment(self):

        new_time_counter = TimeCounter()
        new_time_counter.increment()

        assert new_time_counter.counter == 1

    def test_method_counter_getter(self):

        new_time_counter = TimeCounter()
        new_time_counter.increment()

        result = new_time_counter.counter

        assert result == 1
