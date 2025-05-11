from abc import ABC, abstractmethod
from fractions import Fraction
import math
import re

class TANumber(ABC):
    """Базовый класс для всех типов чисел"""
    
    @abstractmethod
    def add(self, other):
        """Сложение"""
        pass
    
    @abstractmethod
    def subtract(self, other):
        """Вычитание"""
        pass
    
    @abstractmethod
    def multiply(self, other):
        """Умножение"""
        pass
    
    @abstractmethod
    def divide(self, other):
        """Деление"""
        pass
    
    @abstractmethod
    def square(self):
        """Квадрат"""
        pass
    
    @abstractmethod
    def inverse(self):
        """Обратное число"""
        pass
    
    @abstractmethod
    def to_string(self):
        """В строку"""
        pass
    
    @abstractmethod
    def from_string(self, string):
        """Из строки"""
        pass

    @abstractmethod
    def is_zero(self) -> bool:
        """Проверка на ноль"""
        pass

    @abstractmethod
    def copy(self):
        """Копия"""
        pass

    @abstractmethod
    def equals(self, other) -> bool:
        """Сравнение"""
        pass

class TPNumber(TANumber):
    """P-числа (в разных системах счисления)"""
    
    def __init__(self, value=0, base=10):
        self.base = base
        self.value = value
    
    @staticmethod
    def get_allowed_digits(base):
        """Какие цифры можно использовать"""
        if base < 2 or base > 16:
            raise ValueError("Основание от 2 до 16")
        return "0123456789ABCDEF"[:base]
    
    def is_valid_digit(self, digit):
        """Проверка цифры"""
        return digit.upper() in self.get_allowed_digits(self.base)
    
    def add(self, other):
        if not isinstance(other, TPNumber):
            raise TypeError("Только P-числа")
        return TPNumber(self.value + other.value, self.base)
    
    def subtract(self, other):
        if not isinstance(other, TPNumber):
            raise TypeError("Только P-числа")
        return TPNumber(self.value - other.value, self.base)
    
    def multiply(self, other):
        if not isinstance(other, TPNumber):
            raise TypeError("Только P-числа")
        return TPNumber(self.value * other.value, self.base)
    
    def divide(self, other):
        if not isinstance(other, TPNumber):
            raise TypeError("Только P-числа")
        if other.value == 0:
            raise ValueError("На ноль делить нельзя")
        return TPNumber(self.value / other.value, self.base)
    
    def square(self):
        return TPNumber(self.value ** 2, self.base)
    
    def inverse(self):
        if self.value == 0:
            raise ValueError("Ноль нельзя")
        return TPNumber(1 / self.value, self.base)
    
    def to_string(self):
        if self.base == 10:
            # Убираем лишние нули
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
            # Для других систем
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
            # Проверяем на комплексные
            if 'i' in string:
                raise ValueError("Комплексные не поддерживаются")
            
            # Проверяем цифры
            for char in string:
                if char not in self.get_allowed_digits(self.base) and char not in '.-':
                    raise ValueError(f"Неверная цифра '{char}' для основания {self.base}")
            
            self.value = float(string)
        except ValueError as e:
            raise ValueError(f"Неверный формат: {str(e)}")

    def is_zero(self) -> bool:
        return self.value == 0

    def copy(self):
        return TPNumber(self.value, self.base)

    def equals(self, other) -> bool:
        return isinstance(other, TPNumber) and self.value == other.value and self.base == other.base

class TFrac(TANumber):
    """Дроби"""
    
    def __init__(self, numerator=0, denominator=1):
        self.fraction = Fraction(numerator, denominator)
    
    def add(self, other):
        if not isinstance(other, TFrac):
            raise TypeError("Только дроби")
        return TFrac(self.fraction + other.fraction)
    
    def subtract(self, other):
        if not isinstance(other, TFrac):
            raise TypeError("Только дроби")
        return TFrac(self.fraction - other.fraction)
    
    def multiply(self, other):
        if not isinstance(other, TFrac):
            raise TypeError("Только дроби")
        return TFrac(self.fraction * other.fraction)
    
    def divide(self, other):
        if not isinstance(other, TFrac):
            raise TypeError("Только дроби")
        if other.fraction == 0:
            raise ValueError("На ноль делить нельзя")
        return TFrac(self.fraction / other.fraction)
    
    def square(self):
        return TFrac(self.fraction ** 2)
    
    def inverse(self):
        if self.fraction == 0:
            raise ValueError("Ноль нельзя")
        # Меняем местами числитель и знаменатель
        if self.fraction.numerator < 0:
            return TFrac(-self.fraction.denominator, abs(self.fraction.numerator))
        else:
            return TFrac(self.fraction.denominator, self.fraction.numerator)
    
    def to_string(self):
        # Знак всегда в числителе
        if self.fraction.denominator < 0:
            return f"{-self.fraction.numerator}/{abs(self.fraction.denominator)}"
        return f"{self.fraction.numerator}/{self.fraction.denominator}"
    
    def from_string(self, string):
        try:
            if '/' in string:
                # Если дробь
                self.fraction = Fraction(string)
            else:
                # Если целое, добавляем знаменатель 1
                self.fraction = Fraction(int(string), 1)
        except ValueError:
            raise ValueError("Неверный формат дроби")

    def is_zero(self) -> bool:
        return self.fraction == 0

    def copy(self):
        return TFrac(self.fraction.numerator, self.fraction.denominator)

    def equals(self, other) -> bool:
        return isinstance(other, TFrac) and self.fraction == other.fraction

class TComp(TANumber):
    """Комплексные числа"""
    
    def __init__(self, real=0, imag=0):
        self.value = complex(real, imag)
    
    def add(self, other):
        if not isinstance(other, TComp):
            raise TypeError("Только комплексные")
        return TComp(self.value + other.value)
    
    def subtract(self, other):
        if not isinstance(other, TComp):
            raise TypeError("Только комплексные")
        return TComp(self.value - other.value)
    
    def multiply(self, other):
        if not isinstance(other, TComp):
            raise TypeError("Только комплексные")
        return TComp(self.value * other.value)
    
    def divide(self, other):
        if not isinstance(other, TComp):
            raise TypeError("Только комплексные")
        if other.value == 0:
            raise ValueError("На ноль делить нельзя")
        return TComp(self.value / other.value)
    
    def square(self):
        return TComp(self.value ** 2)
    
    def inverse(self):
        if self.value == 0:
            raise ValueError("Ноль нельзя")
        return TComp(1 / self.value)
    
    def to_string(self):
        real = self.value.real
        imag = self.value.imag
        
        # Вещественная часть
        if real == int(real):
            real_str = f"{int(real)}" if real != 0 else ""
        else:
            real_str = f"{real}" if real != 0 else ""
            
        # Мнимая часть
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
                
        # Если обе части ноль
        if real == 0 and imag == 0:
            return "0"
            
        result = f"{real_str}{imag_str}".replace("+-", "-")
        # Убираем + в начале
        if result.startswith("+"):
            result = result[1:]
        return result
    
    def from_string(self, string):
        try:
            # Проверяем на i
            if 'i' not in string:
                raise ValueError("Не комплексное число")
            # Заменяем i на j для Python
            string = string.replace('i', 'j')
            self.value = complex(string)
        except ValueError:
            raise ValueError("Неверный формат комплексного числа")

    def is_zero(self) -> bool:
        return self.value == 0

    def copy(self):
        return TComp(self.value.real, self.value.imag)

    def equals(self, other) -> bool:
        return isinstance(other, TComp) and self.value == other.value 