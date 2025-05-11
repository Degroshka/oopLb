from calc_numbers.TANumber import TPNumber, TFrac, TComp

def test_pnumber():
    # Базовые операции
    a = TPNumber(5)
    b = TPNumber(3)
    assert a.add(b).value == 8
    assert a.subtract(b).value == 2
    assert a.multiply(b).value == 15
    assert a.divide(b).value == 5/3
    assert a.square().value == 25
    assert a.inverse().value == 1/5

    # Проверка нуля
    assert a.is_zero() is False
    assert TPNumber(0).is_zero() is True

    # Проверка копирования и сравнения
    assert a.copy().equals(a)
    assert a.equals(TPNumber(5))
    assert not a.equals(b)

    # Проверка строкового представления
    assert a.to_string() == '5'
    c = TPNumber()
    c.from_string('7')
    assert c.value == 7

    # Проверка разных систем счисления
    d = TPNumber(10, 2)
    assert d.to_string() == '1010'
    e = TPNumber(10, 16)
    assert e.to_string() == 'A'
    f = TPNumber(10, 8)
    assert f.to_string() == '12'

    # Проверка отрицательных чисел
    g = TPNumber(-5)
    assert g.to_string() == '-5'
    assert g.add(TPNumber(3)).value == -2

    # Проверка деления на ноль
    try:
        a.divide(TPNumber(0))
        assert False, "Should raise ValueError"
    except ValueError:
        pass

def test_frac():
    # Базовые операции
    a = TFrac(1, 2)
    b = TFrac(1, 3)
    assert a.add(b).to_string() == '5/6'
    assert a.subtract(b).to_string() == '1/6'
    assert a.multiply(b).to_string() == '1/6'
    assert a.divide(b).to_string() == '3/2'
    assert a.square().to_string() == '1/4'
    assert a.inverse().to_string() == '2/1'

    # Проверка нуля
    assert a.is_zero() is False
    assert TFrac(0, 1).is_zero() is True

    # Проверка копирования и сравнения
    assert a.copy().equals(a)
    assert a.equals(TFrac(1, 2))
    assert not a.equals(b)

    # Проверка строкового представления
    assert a.to_string() == '1/2'
    c = TFrac()
    c.from_string('3/4')
    assert c.to_string() == '3/4'

    # Проверка отрицательных дробей
    d = TFrac(-1, 2)
    assert d.to_string() == '-1/2'
    assert d.add(TFrac(1, 2)).to_string() == '0/1'

    # Проверка деления на ноль
    try:
        a.divide(TFrac(0, 1))
        assert False, "Should raise ValueError"
    except ValueError:
        pass

    # Проверка обратного числа для нуля
    try:
        TFrac(0, 1).inverse()
        assert False, "Should raise ValueError"
    except ValueError:
        pass

def test_comp():
    # Базовые операции
    a = TComp(1, 2)
    b = TComp(3, 4)
    assert a.add(b).to_string() == '4+6i'
    assert a.subtract(b).to_string() == '-2-2i'
    assert a.multiply(b).to_string() == '-5+10i'
    assert a.square().to_string() == '-3+4i'

    # Проверка нуля
    assert a.is_zero() is False
    assert TComp(0, 0).is_zero() is True

    # Проверка копирования и сравнения
    assert a.copy().equals(a)
    assert a.equals(TComp(1, 2))
    assert not a.equals(b)

    # Проверка строкового представления
    assert a.to_string() == '1+2i'
    c = TComp()
    c.from_string('5+6i')
    assert c.equals(TComp(5, 6))

    # Проверка специальных случаев
    d = TComp(2, 0)  # Вещественное число
    assert d.to_string() == '2'
    e = TComp(0, 2)  # Мнимое число
    assert e.to_string() == '2i'
    f = TComp(-1, 0)  # Отрицательное вещественное
    assert f.to_string() == '-1'
    g = TComp(0, -1)  # Отрицательное мнимое
    assert g.to_string() == '-i'

    # Проверка деления
    h = TComp(1, 1)
    i = TComp(1, -1)
    div = h.divide(i)
    assert abs(div.value.real - 0.0) < 1e-10 and abs(div.value.imag - 1.0) < 1e-10

    # Проверка деления на ноль
    try:
        a.divide(TComp(0, 0))
        assert False, "Should raise ValueError"
    except ValueError:
        pass

    # Проверка обратного числа для нуля
    try:
        TComp(0, 0).inverse()
        assert False, "Should raise ValueError"
    except ValueError:
        pass

if __name__ == "__main__":
    test_pnumber()
    test_frac()
    test_comp()
    print("All TANumber tests passed!") 