from memory.UMemory import TMemory
from calc_numbers.TANumber import TPNumber, TFrac, TComp

def test_memory_pnumber():
    m = TMemory(TPNumber(5))
    assert m.state == "Off"
    m.store(TPNumber(10))
    assert m.state == "On"
    assert m.value == "10"
    m.add(TPNumber(2))
    assert m.value == "12"
    m.clear()
    assert m.state == "Off"
    assert m.value == "0"
    m.store(TPNumber(7))
    t = m.take()
    assert t.value == 7
    assert m.state == "On"

def test_memory_frac():
    m = TMemory(TFrac(1, 2))
    assert m.value == "1/2"
    m.store(TFrac(3, 4))
    assert m.value == "3/4"
    m.add(TFrac(1, 4))
    assert m.value == "1/1"
    m.clear()
    assert m.value == "0"

def test_memory_comp():
    m = TMemory(TComp(1, 2))
    assert m.value == "1.0+2.0i"
    m.store(TComp(3, 4))
    assert m.value == "3.0+4.0i"
    m.add(TComp(1, 1))
    assert m.value == "4.0+5.0i"
    m.clear()
    assert m.value == "0"

if __name__ == "__main__":
    test_memory_pnumber()
    test_memory_frac()
    test_memory_comp()
    print("TMemory tests passed!") 