from calc_numbers.TANumber import TPNumber, TFrac, TComp

def test_pnumber():
    a = TPNumber(5)
    b = TPNumber(3)
    assert a.add(b).value == 8
    assert a.subtract(b).value == 2
    assert a.multiply(b).value == 15
    assert a.divide(b).value == 5/3
    assert a.square().value == 25
    assert a.inverse().value == 1/5
    assert a.is_zero() is False
    assert TPNumber(0).is_zero() is True
    assert a.copy().equals(a)
    assert a.equals(TPNumber(5))
    assert not a.equals(b)
    assert a.to_string() == '5'
    c = TPNumber()
    c.from_string('7')
    assert c.value == 7

def test_frac():
    a = TFrac(1, 2)
    b = TFrac(1, 3)
    assert a.add(b).to_string() == '5/6'
    assert a.subtract(b).to_string() == '1/6'
    assert a.multiply(b).to_string() == '1/6'
    assert a.divide(b).to_string() == '3/2'
    assert a.square().to_string() == '1/4'
    assert a.inverse().to_string() == '2/1'
    assert a.is_zero() is False
    assert TFrac(0, 1).is_zero() is True
    assert a.copy().equals(a)
    assert a.equals(TFrac(1, 2))
    assert not a.equals(b)
    assert a.to_string() == '1/2'
    c = TFrac()
    c.from_string('3/4')
    assert c.to_string() == '3/4'

def test_comp():
    a = TComp(1, 2)
    b = TComp(3, 4)
    assert a.add(b).to_string() == '4.0+6.0i'
    assert a.subtract(b).to_string() == '-2.0+-2.0i'
    assert a.multiply(b).to_string() == '-5.0+10.0i'
    assert a.square().to_string() == '-3.0+4.0i'
    assert a.is_zero() is False
    assert TComp(0, 0).is_zero() is True
    assert a.copy().equals(a)
    assert a.equals(TComp(1, 2))
    assert not a.equals(b)
    assert a.to_string() == '1.0+2.0i'
    c = TComp()
    c.from_string('5+6i')
    assert c.equals(TComp(5, 6))
    # Деление и обратное вручную, так как результат комплексный
    d = TComp(2, 0)
    assert d.inverse().to_string() == '0.5+0.0i'
    e = TComp(1, 1)
    f = TComp(1, -1)
    div = e.divide(f)
    assert abs(div.value.real - 0.0) < 1e-10 and abs(div.value.imag - 1.0) < 1e-10

if __name__ == "__main__":
    test_pnumber()
    test_frac()
    test_comp()
    print("All tests passed!") 