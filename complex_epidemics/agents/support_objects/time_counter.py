class TimeCounter:
    def __init__(self, initial_time: int = 0):
        self._counter = initial_time

    @property
    def counter(self) -> int:
        return self._counter

    @counter.setter
    def counter(self, value: int):
        self._counter = value

    def increment(self, amount: int = 1):
        self.counter += amount
