import unittest
from memory.UMemory import TMemory
from calc_numbers.TANumber import TPNumber, TFrac, TComp

class TestMemory(unittest.TestCase):
    def test_pnumber_memory(self):
        memory = TMemory()
        number = TPNumber(5)
        memory.store(number)
        self.assertEqual(memory.value.value, 5)
        memory.add(number)
        self.assertEqual(memory.value.value, 10)
        memory.clear()
        self.assertIsNone(memory.value)

    def test_fraction_memory(self):
        memory = TMemory()
        number = TFrac(1, 2)
        memory.store(number)
        self.assertEqual(memory.value.to_string(), "1/2")
        memory.add(number)
        self.assertEqual(memory.value.to_string(), "1")
        memory.clear()
        self.assertIsNone(memory.value)

    def test_complex_memory(self):
        memory = TMemory()
        number = TComp(1, 2)
        memory.store(number)
        self.assertEqual(memory.value.to_string(), "1+2i")
        memory.add(number)
        self.assertEqual(memory.value.to_string(), "2+4i")
        memory.clear()
        self.assertIsNone(memory.value)

if __name__ == '__main__':
    unittest.main() 