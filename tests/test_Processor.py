from processor.UProcssr import TProc
from calc_numbers.TANumber import TPNumber, TFrac, TComp

def test_processor():
    # Тестирование с P-числами
    proc = TProc()
    proc.lop = TPNumber(5)
    proc.right = TPNumber(3)
    proc.op = "Add"
    proc.op_run()
    assert proc.lop.value == 8

    # Тестирование с дробями
    proc.lop = TFrac(1, 2)
    proc.right = TFrac(1, 3)
    proc.op = "Add"
    proc.op_run()
    assert proc.lop.to_string() == "5/6"

    # Тестирование с комплексными числами
    proc.lop = TComp(1, 2)
    proc.right = TComp(3, 4)
    proc.op = "Add"
    proc.op_run()
    assert proc.lop.to_string() == "4+6i"

if __name__ == "__main__":
    test_processor()
    print("All processor tests passed!") 