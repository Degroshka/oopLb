# Константы
DECIMAL_SEPARATOR = '.'
FRACTION_SEPARATOR = '/'
COMPLEX_SEPARATOR = '+'
IMAGINARY_UNIT = 'i'
ZERO_STRING = '0'

from abc import ABC, abstractmethod

class AEditor(ABC):
    def __init__(self):
        self.string = ZERO_STRING

    def is_zero(self) -> bool:
        return self.string == ZERO_STRING

    @abstractmethod
    def add_sign(self) -> str:
        pass

    @abstractmethod
    def add_digit(self, digit: int) -> str:
        pass

    @abstractmethod
    def add_zero(self) -> str:
        pass

    @abstractmethod
    def add_separator(self) -> str:
        pass

    @abstractmethod
    def backspace(self) -> str:
        pass

    @abstractmethod
    def clear(self) -> str:
        pass

    @abstractmethod
    def edit(self, command) -> str:
        pass

    @property
    def get_string(self) -> str:
        return self.string

    @get_string.setter
    def set_string(self, s: str):
        self.string = s

class PEditor(AEditor):
    def add_sign(self) -> str:
        if self.string.startswith('-'):
            self.string = self.string[1:]
        else:
            self.string = '-' + self.string
        return self.string

    def add_digit(self, digit: int) -> str:
        if self.string == ZERO_STRING:
            self.string = str(digit)
        else:
            self.string += str(digit)
        return self.string

    def add_zero(self) -> str:
        if self.string != ZERO_STRING:
            self.string += '0'
        return self.string

    def add_separator(self) -> str:
        if DECIMAL_SEPARATOR not in self.string:
            self.string += DECIMAL_SEPARATOR
        return self.string

    def backspace(self) -> str:
        if len(self.string) > 1:
            self.string = self.string[:-1]
            if self.string == '-0':
                self.string = ZERO_STRING
        else:
            self.string = ZERO_STRING
        return self.string

    def clear(self) -> str:
        self.string = ZERO_STRING
        return self.string

    def edit(self, command) -> str:
        if command == '+/-':
            return self.add_sign()
        elif command == '0':
            return self.add_zero()
        elif command in '123456789':
            return self.add_digit(int(command))
        elif command == DECIMAL_SEPARATOR:
            return self.add_separator()
        elif command == 'BS':
            return self.backspace()
        elif command == 'C':
            return self.clear()
        else:
            return self.string

class FEditor(AEditor):
    def add_sign(self) -> str:
        if self.string.startswith('-'):
            self.string = self.string[1:]
        else:
            self.string = '-' + self.string
        return self.string

    def add_digit(self, digit: int) -> str:
        if self.string == ZERO_STRING:
            self.string = str(digit)
        else:
            self.string += str(digit)
        return self.string

    def add_zero(self) -> str:
        if self.string != ZERO_STRING:
            self.string += '0'
        return self.string

    def add_separator(self) -> str:
        if FRACTION_SEPARATOR not in self.string:
            self.string += FRACTION_SEPARATOR
        return self.string

    def backspace(self) -> str:
        if len(self.string) > 1:
            self.string = self.string[:-1]
            if self.string == '-0':
                self.string = ZERO_STRING
        else:
            self.string = ZERO_STRING
        return self.string

    def clear(self) -> str:
        self.string = ZERO_STRING
        return self.string

    def edit(self, command) -> str:
        if command == '+/-':
            return self.add_sign()
        elif command == '0':
            return self.add_zero()
        elif command in '123456789':
            return self.add_digit(int(command))
        elif command == FRACTION_SEPARATOR:
            return self.add_separator()
        elif command == 'BS':
            return self.backspace()
        elif command == 'C':
            return self.clear()
        else:
            return self.string

class CEditor(AEditor):
    def add_sign(self) -> str:
        if self.string.startswith('-'):
            self.string = self.string[1:]
        else:
            self.string = '-' + self.string
        return self.string

    def add_digit(self, digit: int) -> str:
        if self.string == ZERO_STRING:
            self.string = str(digit)
        else:
            self.string += str(digit)
        return self.string

    def add_zero(self) -> str:
        if self.string != ZERO_STRING:
            self.string += '0'
        return self.string

    def add_separator(self) -> str:
        if COMPLEX_SEPARATOR not in self.string and '-' not in self.string[1:]:
            self.string += COMPLEX_SEPARATOR
        elif IMAGINARY_UNIT not in self.string:
            self.string += IMAGINARY_UNIT
        return self.string

    def backspace(self) -> str:
        if len(self.string) > 1:
            self.string = self.string[:-1]
            if self.string == '-0':
                self.string = ZERO_STRING
        else:
            self.string = ZERO_STRING
        return self.string

    def clear(self) -> str:
        self.string = ZERO_STRING
        return self.string

    def edit(self, command) -> str:
        if command == '+/-':
            return self.add_sign()
        elif command == '0':
            return self.add_zero()
        elif command in '123456789':
            return self.add_digit(int(command))
        elif command == COMPLEX_SEPARATOR or command == IMAGINARY_UNIT:
            return self.add_separator()
        elif command == 'BS':
            return self.backspace()
        elif command == 'C':
            return self.clear()
        else:
            return self.string 