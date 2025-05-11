from calc_numbers.TANumber import TPNumber

class PEditor:
    """Редактор P-чисел"""
    
    def __init__(self):
        self.number = TPNumber()  # Текущее число
        self.has_separator = False  # Есть точка?
        
    def is_zero(self):
        """Проверка на ноль"""
        return self.number.is_zero()
        
    def add_digit(self, digit):
        """Добавить цифру"""
        if digit == '0' and self.is_zero():
            return
            
        # Если это первая цифра
        if self.is_zero():
            self.number = TPNumber(int(digit))
        else:
            # Добавляем цифру
            if self.has_separator:
                # После точки
                val = self.number.value + int(digit) / (10 ** len(str(self.number.value).split('.')[-1] + '1'))
            else:
                # До точки
                val = self.number.value * 10 + int(digit)
            self.number = TPNumber(val)
            
    def add_separator(self):
        """Добавить точку"""
        if not self.has_separator:
            self.has_separator = True
            
    def backspace(self):
        """Удалить последнюю цифру"""
        if not self.is_zero():
            # Убираем последнюю цифру
            if self.has_separator:
                # После точки
                val = self.number.value
                str_val = str(val)
                if '.' in str_val:
                    parts = str_val.split('.')
                    if len(parts[1]) > 1:
                        val = float(parts[0] + '.' + parts[1][:-1])
                    else:
                        val = float(parts[0])
                        self.has_separator = False
            else:
                # До точки
                val = self.number.value // 10
            self.number = TPNumber(val)
            
    def clear(self):
        """Очистить"""
        self.number = TPNumber()
        self.has_separator = False
        
    def edit(self, number):
        """Редактировать число"""
        self.number = number.copy()
        self.has_separator = '.' in str(self.number.value)
        
    def get_number(self):
        """Получить число"""
        return self.number.copy()
        
    def get_string(self):
        """Получить строку"""
        return self.number.to_string() 