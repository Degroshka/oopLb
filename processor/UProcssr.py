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
    def lop(self) -> TANumber:
        """Читать левый операнд"""
        return self._lop.copy() if self._lop else None
        
    @lop.setter 
    def lop(self, value: TANumber):
        """Записать левый операнд"""
        self._lop = value.copy() if value else None
        
    @property
    def right(self) -> TANumber:
        """Читать правый операнд"""
        return self._rop.copy() if self._rop else None
        
    @right.setter
    def right(self, value: TANumber):
        """Записать правый операнд"""
        self._rop = value.copy() if value else None
        
    @property
    def op(self) -> TOprtn:
        """Читать состояние"""
        return self._operation
        
    @op.setter
    def op(self, value: TOprtn):
        """Записать состояние"""
        self._operation = value
        
    @property
    def error(self) -> str:
        """Читать ошибку"""
        return self._error
        
    def clear_error(self):
        """Сброс ошибки"""
        self._error = ""
        
    def op_run(self):
        """Выполнить операцию"""
        try:
            if not self._lop or not self._rop:
                raise ValueError("Операнды не установлены")
                
            if self._operation == TOprtn.None_:
                raise ValueError("Операция не установлена")
                
            if self._operation == TOprtn.Add:
                self._rop = self._lop.add(self._rop)
            elif self._operation == TOprtn.Sub:
                self._rop = self._lop.subtract(self._rop)
            elif self._operation == TOprtn.Mul:
                self._rop = self._lop.multiply(self._rop)
            elif self._operation == TOprtn.Dvd:
                self._rop = self._lop.divide(self._rop)
                
        except Exception as e:
            self._error = str(e)
            
    def func_run(self, func: TFunc):
        """Выполнить функцию"""
        try:
            if not self._rop:
                raise ValueError("Операнд не установлен")
                
            if func == TFunc.Rev:
                self._rop = self._rop.inverse()
            elif func == TFunc.Sqr:
                self._rop = self._rop.square()
                
        except Exception as e:
            self._error = str(e)
            
    def reset(self):
        """Установить начальное состояние"""
        self._lop = None
        self._rop = None
        self._operation = TOprtn.None_
        self._error = "" 