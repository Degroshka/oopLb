import unittest
from controllers.UControl import TCtrl
from editors.UAEditor import PEditor, FEditor, CEditor

class TestUControl(unittest.TestCase):
    def setUp(self):
        self.ctrl = TCtrl()

    def test_complex_sign_change(self):
        # Тест смены знака для комплексных чисел
        self.ctrl.set_number_type("C")
        
        # Тест с вещественной и мнимой частью
        self.ctrl.expression = "2+3i"
        self.ctrl.command("+/-")
        self.assertEqual(self.ctrl.expression, "-2-3i")
        
        # Тест с отрицательной вещественной частью
        self.ctrl.expression = "-2+3i"
        self.ctrl.command("+/-")
        self.assertEqual(self.ctrl.expression, "2-3i")
        
        # Тест только с мнимой частью
        self.ctrl.expression = "3i"
        self.ctrl.command("+/-")
        self.assertEqual(self.ctrl.expression, "-3i")
        
        # Тест с отрицательной мнимой частью
        self.ctrl.expression = "-3i"
        self.ctrl.command("+/-")
        self.assertEqual(self.ctrl.expression, "3i")

    def test_complex_inverse(self):
        # Тест обратного числа для комплексных чисел
        self.ctrl.set_number_type("C")
        
        # Тест с вещественной и мнимой частью
        self.ctrl.expression = "1+1i"
        self.ctrl.command("1/x")
        self.assertEqual(self.ctrl.expression, "0.5-0.5i")
        
        # Тест только с вещественной частью
        self.ctrl.expression = "2"
        self.ctrl.command("1/x")
        self.assertEqual(self.ctrl.expression, "0.5")
        
        # Тест только с мнимой частью
        self.ctrl.expression = "2i"
        self.ctrl.command("1/x")
        self.assertEqual(self.ctrl.expression, "-0.5i")
        
        # Тест с нулем
        self.ctrl.expression = "0"
        self.ctrl.command("1/x")
        self.assertEqual(self.ctrl.expression, "0")

    def test_fraction_sign_change(self):
        # Тест смены знака для дробей
        self.ctrl.set_number_type("F")
        
        # Тест с положительной дробью
        self.ctrl.expression = "3/4"
        self.ctrl.command("+/-")
        self.assertEqual(self.ctrl.expression, "-3/4")
        
        # Тест с отрицательной дробью
        self.ctrl.expression = "-3/4"
        self.ctrl.command("+/-")
        self.assertEqual(self.ctrl.expression, "3/4")
        
        # Тест с целым числом (должно преобразоваться в дробь)
        self.ctrl.expression = "3"
        self.ctrl.command("+/-")
        self.assertEqual(self.ctrl.expression, "-3/1")

    def test_fraction_inverse(self):
        # Тест обратного числа для дробей
        self.ctrl.set_number_type("F")
        
        # Тест с положительной дробью
        self.ctrl.expression = "3/4"
        self.ctrl.command("1/x")
        self.assertEqual(self.ctrl.expression, "4/3")
        
        # Тест с отрицательной дробью
        self.ctrl.expression = "-3/4"
        self.ctrl.command("1/x")
        self.assertEqual(self.ctrl.expression, "-4/3")
        
        # Тест с целым числом
        self.ctrl.expression = "3"
        self.ctrl.command("1/x")
        self.assertEqual(self.ctrl.expression, "1/3")
        
        # Тест с нулем
        self.ctrl.expression = "0"
        self.ctrl.command("1/x")
        self.assertEqual(self.ctrl.expression, "0")

    def test_power_operation(self):
        # Тест операции возведения в степень
        self.ctrl.set_number_type("P")
        
        # Тест с положительными числами
        self.ctrl.expression = "2"
        self.ctrl.command("^")
        self.ctrl.expression += " 3"
        self.ctrl.command("=")
        self.assertEqual(self.ctrl.expression, "8")
        
        # Тест с отрицательным основанием
        self.ctrl.expression = "-2"
        self.ctrl.command("^")
        self.ctrl.expression += " 3"
        self.ctrl.command("=")
        self.assertEqual(self.ctrl.expression, "-8")
        
        # Тест с нулевой степенью
        self.ctrl.expression = "2"
        self.ctrl.command("^")
        self.ctrl.expression += " 0"
        self.ctrl.command("=")
        self.assertEqual(self.ctrl.expression, "1")
        
        # Тест с отрицательной степенью
        self.ctrl.expression = "2"
        self.ctrl.command("^")
        self.ctrl.expression += " -2"
        self.ctrl.command("=")
        self.assertEqual(self.ctrl.expression, "0.25")

if __name__ == '__main__':
    unittest.main() 