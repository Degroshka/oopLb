import unittest
from processor.UProcssr import TProc, TOprtn
from calc_numbers.TANumber import TPNumber, TFrac, TComp

class TestProcessor(unittest.TestCase):
    def test_pnumber_operations(self):
        # Тестирование с P-числами
        proc = TProc()
        proc.lop = TPNumber(5)
        proc.right = TPNumber(3)
        proc.op = TOprtn.Add
        proc.op_run()
        self.assertEqual(proc.right.value, 8)

    def test_fraction_operations(self):
        # Тестирование с дробями
        proc = TProc()
        proc.lop = TFrac(1, 2)
        proc.right = TFrac(1, 3)
        proc.op = TOprtn.Add
        proc.op_run()
        self.assertEqual(proc.right.to_string(), "5/6")

    def test_complex_operations(self):
        # Тестирование с комплексными числами
        proc = TProc()
        proc.lop = TComp(1, 2)
        proc.right = TComp(3, 4)
        proc.op = TOprtn.Add
        proc.op_run()
        self.assertEqual(proc.right.to_string(), "4+6i")

if __name__ == '__main__':
    unittest.main() 