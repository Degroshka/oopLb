from calc_numbers.TANumber import TANumber

class TMemory:
    """Память калькулятора"""
    
    def __init__(self):
        self.value = None  # Значение в памяти
        
    def store(self, number):
        """Сохранить число"""
        self.value = number.copy()
        
    def add(self, number):
        """Добавить число"""
        if self.value:
            self.value = self.value.add(number)
        else:
            self.value = number.copy()
            
    def clear(self):
        """Очистить память"""
        self.value = None
        
    def get(self):
        """Получить число"""
        return self.value.copy() if self.value else None 