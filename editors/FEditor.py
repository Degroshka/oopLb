from calc_numbers.TANumber import TFrac

class FEditor:
    """Редактор дробей"""
    
    def __init__(self):
        self.number = TFrac()  # Текущее число
        
    def is_zero(self):
        """Проверка на ноль"""
        return self.number.is_zero()
        
    def add_digit(self, digit):
        """Добавить цифру"""
        if digit == '0':
            return
            
        # Если это первая цифра
        if self.is_zero():
            self.number = TFrac(int(digit), 1)
        else:
            # Добавляем цифру к числителю
            num = self.number.fraction.numerator * 10 + int(digit)
            self.number = TFrac(num, self.number.fraction.denominator)
            
    def add_separator(self):
        """Добавить разделитель"""
        # Для дробей не нужно
        pass
        
    def backspace(self):
        """Удалить последнюю цифру"""
        if not self.is_zero():
            # Убираем последнюю цифру из числителя
            num = self.number.fraction.numerator // 10
            self.number = TFrac(num, self.number.fraction.denominator)
            
    def clear(self):
        """Очистить"""
        self.number = TFrac()
        
    def edit(self, number):
        """Редактировать число"""
        self.number = number.copy()
        
    def get_number(self):
        """Получить число"""
        return self.number.copy()
        
    def get_string(self):
        """Получить строку"""
        return self.number.to_string() 