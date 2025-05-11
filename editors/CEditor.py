from calc_numbers.TANumber import TComp

class CEditor:
    """Редактор комплексных чисел"""
    
    def __init__(self):
        self.number = TComp()  # Текущее число
        self.is_imaginary = False  # Редактируем мнимую часть?
        
    def is_zero(self):
        """Проверка на ноль"""
        return self.number.is_zero()
        
    def add_digit(self, digit):
        """Добавить цифру"""
        if digit == '0':
            return
            
        # Если это первая цифра
        if self.is_zero():
            if self.is_imaginary:
                self.number = TComp(0, int(digit))
            else:
                self.number = TComp(int(digit), 0)
        else:
            # Добавляем цифру к нужной части
            if self.is_imaginary:
                real = self.number.value.real
                imag = self.number.value.imag * 10 + int(digit)
                self.number = TComp(real, imag)
            else:
                real = self.number.value.real * 10 + int(digit)
                imag = self.number.value.imag
                self.number = TComp(real, imag)
            
    def add_separator(self):
        """Добавить разделитель"""
        # Для комплексных чисел не нужно
        pass
        
    def backspace(self):
        """Удалить последнюю цифру"""
        if not self.is_zero():
            # Убираем последнюю цифру из нужной части
            if self.is_imaginary:
                real = self.number.value.real
                imag = self.number.value.imag // 10
                self.number = TComp(real, imag)
            else:
                real = self.number.value.real // 10
                imag = self.number.value.imag
                self.number = TComp(real, imag)
            
    def clear(self):
        """Очистить"""
        self.number = TComp()
        self.is_imaginary = False
        
    def edit(self, number):
        """Редактировать число"""
        self.number = number.copy()
        
    def get_number(self):
        """Получить число"""
        return self.number.copy()
        
    def get_string(self):
        """Получить строку"""
        return self.number.to_string()
        
    def toggle_imaginary(self):
        """Переключить мнимую часть"""
        self.is_imaginary = not self.is_imaginary 