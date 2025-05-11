from calc_numbers.TANumber import TANumber

class TProc:
    """Процессор калькулятора"""
    
    def __init__(self):
        self.lop = None  # Левое число
        self.right = None  # Правое число
        self.op = None  # Операция
        
    def op_run(self):
        """Выполнить операцию"""
        if not self.lop or not self.right or not self.op:
            return
            
        if self.op == "Add":
            self.lop = self.lop.add(self.right)
        elif self.op == "Sub":
            self.lop = self.lop.subtract(self.right)
        elif self.op == "Mul":
            self.lop = self.lop.multiply(self.right)
        elif self.op == "Div":
            self.lop = self.lop.divide(self.right)
        elif self.op == "Sqr":
            self.lop = self.lop.square()
        elif self.op == "Rev":
            self.lop = self.lop.inverse()
            
    def op_run_memory(self, memory):
        """Выполнить операцию с памятью"""
        if not self.lop or not memory or not self.op:
            return
            
        if self.op == "Add":
            self.lop = self.lop.add(memory)
        elif self.op == "Sub":
            self.lop = self.lop.subtract(memory)
        elif self.op == "Mul":
            self.lop = self.lop.multiply(memory)
        elif self.op == "Div":
            self.lop = self.lop.divide(memory)
            
    def clear(self):
        """Очистить"""
        self.lop = None
        self.right = None
        self.op = None 