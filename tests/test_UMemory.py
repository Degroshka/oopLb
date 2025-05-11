from memory.UMemory import TMemory
from calc_numbers.TANumber import TPNumber, TFrac, TComp

def test_memory_pnumber():
    # Инициализация
    m = TMemory(TPNumber(5))
    assert m.state == "Off"
    assert m.value == "5"

    # Сохранение значения
    m.store(TPNumber(10))
    assert m.state == "On"
    assert m.value == "10"

    # Добавление к значению
    m.add(TPNumber(2))
    assert m.value == "12"

    # Очистка памяти
    m.clear()
    assert m.state == "Off"
    assert m.value == "0"

    # Получение значения
    m.store(TPNumber(7))
    t = m.take()
    assert t.value == 7
    assert m.state == "On"

    # Проверка с отрицательными числами
    m.store(TPNumber(-5))
    assert m.value == "-5"
    m.add(TPNumber(3))
    assert m.value == "-2"

def test_memory_frac():
    # Инициализация
    m = TMemory(TFrac(1, 2))
    assert m.value == "1/2"

    # Сохранение значения
    m.store(TFrac(3, 4))
    assert m.value == "3/4"

    # Добавление к значению
    m.add(TFrac(1, 4))
    assert m.value == "1/1"

    # Очистка памяти
    m.clear()
    assert m.value == "0"

    # Проверка с отрицательными дробями
    m.store(TFrac(-1, 2))
    assert m.value == "-1/2"
    m.add(TFrac(1, 2))
    assert m.value == "0/1"

    # Проверка с нулевой дробью
    m.store(TFrac(0, 1))
    assert m.value == "0/1"

def test_memory_comp():
    # Инициализация
    m = TMemory(TComp(1, 2))
    assert m.value == "1+2i"

    # Сохранение значения
    m.store(TComp(3, 4))
    assert m.value == "3+4i"

    # Добавление к значению
    m.add(TComp(1, 1))
    assert m.value == "4+5i"

    # Очистка памяти
    m.clear()
    assert m.value == "0"

    # Проверка с вещественными числами
    m.store(TComp(2, 0))
    assert m.value == "2"
    m.add(TComp(3, 0))
    assert m.value == "5"

    # Проверка с мнимыми числами
    m.store(TComp(0, 2))
    assert m.value == "2i"
    m.add(TComp(0, 3))
    assert m.value == "5i"

    # Проверка с отрицательными числами
    m.store(TComp(-1, -2))
    assert m.value == "-1-2i"
    m.add(TComp(1, 2))
    assert m.value == "0"

def test_memory_state_transitions():
    # Проверка переходов состояния памяти
    m = TMemory()
    assert m.state == "Off"
    assert m.value == "0"

    # Включение памяти
    m.store(TPNumber(1))
    assert m.state == "On"
    assert m.value == "1"

    # Выключение памяти
    m.clear()
    assert m.state == "Off"
    assert m.value == "0"

    # Повторное включение
    m.store(TPNumber(2))
    assert m.state == "On"
    assert m.value == "2"

    # Получение значения не меняет состояние
    val = m.take()
    assert m.state == "On"
    assert val.value == 2

if __name__ == "__main__":
    test_memory_pnumber()
    test_memory_frac()
    test_memory_comp()
    test_memory_state_transitions()
    print("All TMemory tests passed!") 