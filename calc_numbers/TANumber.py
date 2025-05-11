from abc import ABC, abstractmethod
from fractions import Fraction
import math
import re

class TANumber(ABC):
    """Abstract base class for all number types"""
    
    @abstractmethod
    def add(self, other):
        """Add two numbers"""
        pass
    
    @abstractmethod
    def subtract(self, other):
        """Subtract two numbers"""
        pass
    
    @abstractmethod
    def multiply(self, other):
        """Multiply two numbers"""
        pass
    
    @abstractmethod
    def divide(self, other):
        """Divide two numbers"""
        pass
    
    @abstractmethod
    def square(self):
        """Square the number"""
        pass
    
    @abstractmethod
    def inverse(self):
        """Get the inverse of the number"""
        pass
    
    @abstractmethod
    def to_string(self):
        """Convert number to string representation"""
        pass
    
    @abstractmethod
    def from_string(self, string):
        """Create number from string representation"""
        pass

    @abstractmethod
    def is_zero(self) -> bool:
        pass

    @abstractmethod
    def copy(self):
        pass

    @abstractmethod
    def equals(self, other) -> bool:
        pass

class TPNumber(TANumber):
    """P-based number implementation"""
    
    def __init__(self, value=0, base=10):
        self.base = base
        self.value = value
    
    @staticmethod
    def get_allowed_digits(base):
        """Возвращает список допустимых цифр для данной системы счисления"""
        if base < 2 or base > 16:
            raise ValueError("Base must be between 2 and 16")
        return "0123456789ABCDEF"[:base]
    
    def is_valid_digit(self, digit):
        """Проверяет, является ли символ допустимой цифрой для текущей системы счисления"""
        return digit.upper() in self.get_allowed_digits(self.base)
    
    def add(self, other):
        if not isinstance(other, TPNumber):
            raise TypeError("Can only add TPNumber")
        return TPNumber(self.value + other.value, self.base)
    
    def subtract(self, other):
        if not isinstance(other, TPNumber):
            raise TypeError("Can only subtract TPNumber")
        return TPNumber(self.value - other.value, self.base)
    
    def multiply(self, other):
        if not isinstance(other, TPNumber):
            raise TypeError("Can only multiply TPNumber")
        return TPNumber(self.value * other.value, self.base)
    
    def divide(self, other):
        if not isinstance(other, TPNumber):
            raise TypeError("Can only divide TPNumber")
        if other.value == 0:
            raise ValueError("Division by zero")
        return TPNumber(self.value / other.value, self.base)
    
    def square(self):
        return TPNumber(self.value ** 2, self.base)
    
    def inverse(self):
        if self.value == 0:
            raise ValueError("Cannot inverse zero")
        return TPNumber(1 / self.value, self.base)
    
    def to_string(self):
        if self.base == 10:
            # Убираем незначащие нули
            if self.value == int(self.value):
                return str(int(self.value))
            return str(self.value)
        elif self.base == 2:
            return bin(int(self.value))[2:]
        elif self.base == 8:
            return oct(int(self.value))[2:]
        elif self.base == 16:
            return hex(int(self.value))[2:].upper()
        else:
            # Для других систем счисления
            if self.value == 0:
                return "0"
            num = int(self.value)
            digits = []
            while num:
                digits.append(self.get_allowed_digits(self.base)[num % self.base])
                num //= self.base
            return ''.join(reversed(digits))
    
    def from_string(self, string):
        try:
            # Проверяем, не является ли число комплексным
            if 'i' in string:
                raise ValueError("Complex numbers are not supported in P-numbers")
            
            # Проверяем все символы на допустимость в текущей системе счисления
            for char in string:
                if char not in self.get_allowed_digits(self.base) and char not in '.-':
                    raise ValueError(f"Invalid digit '{char}' for base {self.base}")
            
            self.value = float(string)
        except ValueError as e:
            raise ValueError(f"Invalid number format: {str(e)}")

    def is_zero(self) -> bool:
        return self.value == 0

    def copy(self):
        return TPNumber(self.value, self.base)

    def equals(self, other) -> bool:
        return isinstance(other, TPNumber) and self.value == other.value and self.base == other.base

class TFrac(TANumber):
    """Fraction implementation"""
    
    def __init__(self, numerator=0, denominator=1):
        self.fraction = Fraction(numerator, denominator)
    
    def add(self, other):
        if not isinstance(other, TFrac):
            raise TypeError("Can only add TFrac")
        return TFrac(self.fraction + other.fraction)
    
    def subtract(self, other):
        if not isinstance(other, TFrac):
            raise TypeError("Can only subtract TFrac")
        return TFrac(self.fraction - other.fraction)
    
    def multiply(self, other):
        if not isinstance(other, TFrac):
            raise TypeError("Can only multiply TFrac")
        return TFrac(self.fraction * other.fraction)
    
    def divide(self, other):
        if not isinstance(other, TFrac):
            raise TypeError("Can only divide TFrac")
        if other.fraction == 0:
            raise ValueError("Division by zero")
        return TFrac(self.fraction / other.fraction)
    
    def square(self):
        return TFrac(self.fraction ** 2)
    
    def inverse(self):
        if self.fraction == 0:
            raise ValueError("Cannot inverse zero")
        return TFrac(1 / self.fraction)
    
    def to_string(self):
        return f"{self.fraction.numerator}/{self.fraction.denominator}"
    
    def from_string(self, string):
        try:
            self.fraction = Fraction(string)
        except ValueError:
            raise ValueError("Invalid fraction format")

    def is_zero(self) -> bool:
        return self.fraction == 0

    def copy(self):
        return TFrac(self.fraction.numerator, self.fraction.denominator)

    def equals(self, other) -> bool:
        return isinstance(other, TFrac) and self.fraction == other.fraction

class TComp(TANumber):
    """Complex number implementation"""
    
    def __init__(self, real=0, imag=0):
        self.value = complex(real, imag)
    
    def add(self, other):
        if not isinstance(other, TComp):
            raise TypeError("Can only add TComp")
        return TComp(self.value + other.value)
    
    def subtract(self, other):
        if not isinstance(other, TComp):
            raise TypeError("Can only subtract TComp")
        return TComp(self.value - other.value)
    
    def multiply(self, other):
        if not isinstance(other, TComp):
            raise TypeError("Can only multiply TComp")
        return TComp(self.value * other.value)
    
    def divide(self, other):
        if not isinstance(other, TComp):
            raise TypeError("Can only divide TComp")
        if other.value == 0:
            raise ValueError("Division by zero")
        return TComp(self.value / other.value)
    
    def square(self):
        return TComp(self.value ** 2)
    
    def inverse(self):
        if self.value == 0:
            raise ValueError("Cannot inverse zero")
        return TComp(1 / self.value)
    
    def to_string(self):
        real = self.value.real
        imag = self.value.imag
        
        # Форматируем вещественную часть
        if real == int(real):
            real_str = f"{int(real)}" if real != 0 else ""
        else:
            real_str = f"{real}" if real != 0 else ""
            
        # Форматируем мнимую часть
        if imag == 0:
            imag_str = ""
        elif imag == 1:
            imag_str = "+i" if real != 0 else "i"
        elif imag == -1:
            imag_str = "-i"
        elif imag > 0:
            if imag == int(imag):
                imag_str = f"+{int(imag)}i" if real != 0 else f"{int(imag)}i"
            else:
                imag_str = f"+{imag}i" if real != 0 else f"{imag}i"
        else:  # imag < 0
            if imag == int(imag):
                imag_str = f"{int(imag)}i"
            else:
                imag_str = f"{imag}i"
                
        # Если обе части ноль, выводим 0
        if real == 0 and imag == 0:
            return "0"
            
        result = f"{real_str}{imag_str}".replace("+-", "-")
        # Если результат начинается с +, убираем его
        if result.startswith("+"):
            result = result[1:]
        return result
    
    def from_string(self, string):
        try:
            # Проверяем наличие i для определения комплексного числа
            if 'i' not in string:
                raise ValueError("Not a complex number")
            # Replace i with j for Python's complex number support
            string = string.replace('i', 'j')
            self.value = complex(string)
        except ValueError:
            raise ValueError("Invalid complex number format")

    def is_zero(self) -> bool:
        return self.value == 0

    def copy(self):
        return TComp(self.value.real, self.value.imag)

    def equals(self, other) -> bool:
        return isinstance(other, TComp) and self.value == other.value 