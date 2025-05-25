from enum import Enum
from calc_numbers.TANumber import TANumber

class TOprtn(Enum):
    """Двухоперандные операции"""
    None_ = 0
    Add = 1
    Sub = 2
    Mul = 3
    Dvd = 4

class TFunc(Enum):
    """Однооперандные операции - функции"""
    Rev = 0
    Sqr = 1

class TProc:
    """Процессор калькулятора"""
    
    def __init__(self):
        self._lop = None  # Левое число
        self._rop = None  # Правое число
        self._operation = TOprtn.None_  # Текущая операция
        self._error = ""  # Сообщение об ошибке
        
    @property
    def lop(self):
        return self._lop

    @lop.setter
    def lop(self, value):
        self._lop = value
        
    @property
    def right(self):
        return self._rop
        
    @right.setter
    def right(self, value):
        self._rop = value
        
    @property
    def op(self):
        return self._operation
        
    @op.setter
    def op(self, value):
        self._operation = value
        
    @property
    def error(self):
        return self._error
        
    def clear_error(self):
        self._error = ""
        
    def op_run(self):
        if self._operation == TOprtn.Add:
            self._lop = self._lop.add(self._rop)
        elif self._operation == TOprtn.Sub:
            self._lop = self._lop.subtract(self._rop)
        elif self._operation == TOprtn.Mul:
            self._lop = self._lop.multiply(self._rop)
        elif self._operation == TOprtn.Dvd:
            self._lop = self._lop.divide(self._rop)
            
    def func_run(self, func):
        if func == TFunc.Rev:
            self._rop = self._rop.inverse()
        elif func == TFunc.Sqr:
            self._rop = self._rop.square()
            
    def reset(self):
        self._lop = None
        self._rop = None
        self._operation = TOprtn.None_
        self._error = "" 