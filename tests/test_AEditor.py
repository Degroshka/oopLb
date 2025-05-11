from editors.UAEditor import PEditor, FEditor, CEditor

def test_peditor():
    ed = PEditor()
    ed.add_digit(5)
    assert ed.get_string() == "5"
    ed.add_sign()
    assert ed.get_string() == "-5"
    ed.add_separator()
    ed.add_digit(3)
    assert ed.get_string() == "-5.3"
    ed.backspace()
    assert ed.get_string() == "-5."
    ed.clear()
    assert ed.get_string() == "0"
    ed.edit("1")
    ed.edit("2")
    ed.edit("+/-")
    assert ed.get_string() == "-12"
    ed.edit("C")
    assert ed.get_string() == "0"

def test_feditor():
    ed = FEditor()
    ed.add_digit(1)
    ed.add_separator()
    ed.add_digit(2)
    assert ed.get_string() == "1/2"
    ed.add_sign()
    assert ed.get_string() == "-1/2"
    ed.backspace()
    assert ed.get_string() == "-1/"
    ed.clear()
    assert ed.get_string() == "0"
    ed.edit("3")
    ed.edit("/")
    ed.edit("4")
    assert ed.get_string() == "3/4"
    ed.edit("+/-")
    assert ed.get_string() == "-3/4"
    ed.edit("C")
    assert ed.get_string() == "0"

def test_ceditor():
    ed = CEditor()
    ed.add_digit(2)
    ed.add_separator()  # +
    ed.add_digit(3)
    ed.add_separator()  # i
    assert ed.get_string() == "2+3i"
    ed.add_sign()
    assert ed.get_string() == "-2+3i"
    ed.backspace()
    assert ed.get_string() == "-2+3"
    ed.clear()
    assert ed.get_string() == "0"
    ed.edit("1")
    ed.edit("+")
    ed.edit("2")
    ed.edit("i")
    assert ed.get_string() == "1+2i"
    ed.edit("+/-")
    assert ed.get_string() == "-1+2i"
    ed.edit("C")
    assert ed.get_string() == "0"

if __name__ == "__main__":
    test_peditor()
    test_feditor()
    test_ceditor()
    print("All AEditor tests passed!") 