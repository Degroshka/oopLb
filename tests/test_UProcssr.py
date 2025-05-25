from processor.UProcssr import TProc, TOprtn, TFunc
from calc_numbers.TANumber import TPNumber, TFrac, TComp

def test_proc_pnumber():
    p = TProc(TPNumber(2), TPNumber(3))
    assert p.lop.value == 2
    assert p.right.value == 3
    p.op = TOprtn.Add
    p.op_run()
    assert p.lop.value == 5
    p.right = TPNumber(4)
    p.op = TOprtn.Mul
    p.op_run()
    assert p.lop.value == 20
    p.func_run(TFunc.Sqr)
    assert p.right.value == 16
    p.func_run(TFunc.Rev)
    assert abs(p.right.value - 1/16) < 1e-10
    p.reset()
    assert p.lop.value == 0 and p.right.value == 0 and p.op == TOprtn.None_

def test_proc_frac():
    p = TProc(TFrac(1, 2), TFrac(1, 3))
    p.op = TOprtn.Add
    p.op_run()
    assert p.lop.to_string() == "5/6"
    p.right = TFrac(1, 6)
    p.op = TOprtn.Sub
    p.op_run()
    assert p.lop.to_string() == "2/3"
    p.right = TFrac(2, 1)
    p.op = TOprtn.Mul
    p.op_run()
    assert p.lop.to_string() == "4/3"
    p.right = TFrac(2, 1)
    p.op = TOprtn.Dvd
    p.op_run()
    assert p.lop.to_string() == "2/3"
    p.func_run(TFunc.Sqr)
    assert p.right.to_string() == "4/9"
    p.func_run(TFunc.Rev)
    assert p.right.to_string() == "9/4"
    p.reset()
    assert p.lop.to_string() == "0/1" and p.right.to_string() == "0/1" and p.op == TOprtn.None_

def test_proc_comp():
    p = TProc(TComp(1, 2), TComp(3, 4))
    p.op = TOprtn.Add
    p.op_run()
    assert p.lop.to_string() == "4.0+6.0i"
    p.right = TComp(1, 1)
    p.op = TOprtn.Mul
    p.op_run()
    assert p.lop.to_string() == "-2.0+10.0i"
    p.func_run(TFunc.Sqr)
    assert p.right.to_string() == "0.0+2.0i"
    p.func_run(TFunc.Rev)
    # Проверка обратного значения комплексного числа
    inv = p.right
    assert abs(inv.value.real - 0.0) < 1e-10 and abs(inv.value.imag - -0.5) < 1e-10
    p.reset()
    assert p.lop.to_string() == "0.0+0.0i" and p.right.to_string() == "0.0+0.0i" and p.op == TOprtn.None_

if __name__ == "__main__":
    test_proc_pnumber()
    test_proc_frac()
    test_proc_comp()
    print("TProc tests passed!") 