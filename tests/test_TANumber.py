import unittest
from calc_numbers.TANumber import TPNumber, TFrac, TComp

class TestNumbers(unittest.TestCase):
    def test_pnumber_operations(self):
        num1 = TPNumber(5)
        num2 = TPNumber(3)
        self.assertEqual((num1 + num2).value, 8)
        self.assertEqual((num1 - num2).value, 2)
        self.assertEqual((num1 * num2).value, 15)
        self.assertEqual((num1 / num2).value, 5/3)

    def test_fraction_operations(self):
        num1 = TFrac(1, 2)
        num2 = TFrac(1, 3)
        self.assertEqual((num1 + num2).to_string(), "5/6")
        self.assertEqual((num1 - num2).to_string(), "1/6")
        self.assertEqual((num1 * num2).to_string(), "1/6")
        self.assertEqual((num1 / num2).to_string(), "3/2")

    def test_complex_operations(self):
        num1 = TComp(1, 2)
        num2 = TComp(3, 4)
        self.assertEqual((num1 + num2).to_string(), "4+6i")
        self.assertEqual((num1 - num2).to_string(), "-2-2i")
        self.assertEqual((num1 * num2).to_string(), "-5+10i")
        self.assertEqual((num1 / num2).to_string(), "0.44+0.08i")

if __name__ == '__main__':
    unittest.main() 