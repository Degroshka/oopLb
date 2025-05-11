from calc_numbers.TANumber import TANumber, TPNumber

class TMemory:
    _ON = "On"
    _OFF = "Off"

    def __init__(self, number: TANumber = None):
        if number is None:
            number = TPNumber(0)
        self.mem = number.copy()
        self._state = self._OFF

    def store(self, number: TANumber):
        self.mem = number.copy()
        self._state = self._ON

    def take(self) -> TANumber:
        self._state = self._ON
        return self.mem.copy()

    def add(self, number: TANumber):
        self.mem = self.mem.add(number)
        self._state = self._ON

    def clear(self):
        self.mem = TPNumber(0)
        self._state = self._OFF

    @property
    def state(self) -> str:
        return self._state

    @property
    def value(self) -> str:
        return self.mem.to_string() 