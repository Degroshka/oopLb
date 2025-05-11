from calc_numbers.TANumber import TANumber, TPNumber

class TProc:
    def __init__(self, lop: TANumber = None, rop: TANumber = None):
        self.lop_res = lop.copy() if lop else TPNumber(0)
        self.rop = rop.copy() if rop else TPNumber(0)
        self.operation = None
        self.error = ""

    def reset(self):
        self.lop_res = TPNumber(0)
        self.rop = TPNumber(0)
        self.operation = None
        self.error = ""

    def op_clear(self):
        self.operation = None

    def op_run(self):
        if self.operation is None:
            return
        try:
            if self.operation == "Add":
                self.lop_res = self.lop_res.add(self.rop)
            elif self.operation == "Sub":
                self.lop_res = self.lop_res.subtract(self.rop)
            elif self.operation == "Mul":
                self.lop_res = self.lop_res.multiply(self.rop)
            elif self.operation == "Dvd":
                self.lop_res = self.lop_res.divide(self.rop)
            self.error = ""
        except Exception as e:
            self.error = str(e)

    def func_run(self, func):
        try:
            if func == "Rev":
                self.rop = self.rop.inverse()
            elif func == "Sqr":
                self.rop = self.rop.square()
            self.error = ""
        except Exception as e:
            self.error = str(e)

    @property
    def lop(self):
        return self.lop_res.copy()

    @lop.setter
    def lop(self, operand):
        self.lop_res = operand.copy()

    @property
    def right(self):
        return self.rop.copy()

    @right.setter
    def right(self, operand):
        self.rop = operand.copy()

    @property
    def op(self):
        return self.operation

    @op.setter
    def op(self, value):
        self.operation = value

    @property
    def err(self):
        return self.error

    def error_clear(self):
        self.error = "" 