from enum import Enum
from editors.UAEditor import PEditor, FEditor, CEditor, AEditor
from processor.UProcssr import TProc
from memory.UMemory import TMemory
from calc_numbers.TANumber import TANumber, TPNumber

class TCtrlState(Enum):
    cStart = 0
    cEditing = 1
    FunDone = 2
    cValDone = 3
    cExpDone = 4
    cOpChange = 5
    cError = 6

class TCtrl:
    def __init__(self, editor: AEditor = None):
        self.state: TCtrlState = TCtrlState.cStart
        self.editor: AEditor = editor if editor else PEditor()
        self.proc: TProc = TProc()
        self.memory: TMemory = TMemory()
        self.number: TANumber = TPNumber(0)
        self.expression: str = ""
        self.current_base = 10  # Добавляем текущую систему счисления

    def execute_calculator_command(self, command: int, clipboard: str, mem_state: str) -> tuple[str, str, str]:
        if 0 <= command <= 9:
            result = self.execute_editor_command(command)
            self.state = TCtrlState.cEditing
        elif 10 <= command <= 19:
            result = self.execute_operation(command)
            self.state = TCtrlState.cOpChange
        elif 20 <= command <= 29:
            mem_state, result = self.execute_memory_command(command, mem_state)
        elif 30 <= command <= 39:
            result = self.execute_function(command)
            self.state = TCtrlState.FunDone
        elif 40 <= command <= 49:
            result = self.evaluate_expression(command)
            self.state = TCtrlState.cExpDone
        else:
            result = "Unknown command"
            self.state = TCtrlState.cError
        return clipboard, mem_state, result

    def execute_editor_command(self, command: int) -> str:
        if 0 <= command <= 9:
            return self.editor.add_digit(command)
        elif command == 10:
            return self.editor.add_sign()
        elif command == 11:
            return self.editor.add_separator()
        elif command == 12:
            return self.editor.backspace()
        elif command == 13:
            return self.editor.clear()
        else:
            return self.editor.get_string

    def execute_operation(self, command: int) -> str:
        op_map = {10: "Add", 11: "Sub", 12: "Mul", 13: "Dvd"}
        op = op_map.get(command)
        if op:
            self.proc.op = op
            self.proc.right = TPNumber(float(self.editor.get_string))
            self.proc.op_run()
            self.number = self.proc.lop
            return self.number.to_string()
        return "Invalid operation"

    def execute_function(self, command: int) -> str:
        func_map = {30: "Rev", 31: "Sqr"}
        func = func_map.get(command)
        if func:
            self.proc.func_run(func)
            return self.proc.right.to_string()
        return "Invalid function"

    def evaluate_expression(self, command: int) -> str:
        if command == 40:
            self.proc.op_run()
            self.number = self.proc.lop
            return self.number.to_string()
        return "Invalid expression command"

    def set_initial_state(self, command: int = 0) -> str:
        self.state = TCtrlState.cStart
        self.editor.clear()
        self.proc.reset()
        self.memory.clear()
        self.number = TPNumber(0)
        return "start_state"

    def execute_memory_command(self, command: int, mem_state: str) -> tuple[str, str]:
        if command == 20:
            self.memory.store(self.number)
            mem_state = "On"
            return mem_state, "Stored"
        elif command == 21:
            num = self.memory.take()
            return mem_state, num.to_string()
        elif command == 22:
            self.memory.add(self.number)
            return mem_state, "Added"
        elif command == 23:
            self.memory.clear()
            mem_state = "Off"
            return mem_state, "Cleared"
        return mem_state, "Invalid memory command"

    def execute_clipboard_command(self, command: int, clipboard: str) -> tuple[str, str]:
        if command == 50:
            clipboard = self.editor.get_string
            return clipboard, "Copied"
        elif command == 51:
            self.editor.set_string = clipboard
            return clipboard, "Pasted"
        return clipboard, "Invalid clipboard command"

    @property
    def ctrl_state(self) -> TCtrlState:
        return self.state

    @ctrl_state.setter
    def ctrl_state(self, value: TCtrlState):
        self.state = value

    def set_number_type(self, type_str: str):
        if type_str == "P":
            self.editor = PEditor()
        elif type_str == "F":
            self.editor = FEditor()
        elif type_str == "C":
            self.editor = CEditor()
        else:
            raise ValueError(f"Unknown number type: {type_str}")

    def __del__(self):
        pass

    def set_base(self, base: int):
        """Установка системы счисления"""
        self.current_base = base
        # Конвертируем текущее выражение в новую систему
        if self.expression:
            try:
                # Если выражение содержит только число
                if all(c in "0123456789ABCDEF" for c in self.expression):
                    dec_value = int(self.expression, self.current_base)
                    if base == 10:
                        self.expression = str(dec_value)
                    elif base == 16:
                        self.expression = hex(dec_value)[2:].upper()
                    elif base == 8:
                        self.expression = oct(dec_value)[2:]
                    elif base == 2:
                        self.expression = bin(dec_value)[2:]
                    else:
                        digits = []
                        n = dec_value
                        while n:
                            digits.append("0123456789ABCDEF"[n % base])
                            n //= base
                        self.expression = ''.join(reversed(digits)) if digits else '0'
            except ValueError:
                pass

    def command(self, cmd: str):
        try:
            # Ввод символов в выражение
            if cmd in "0123456789ABCDEFabcdef":
                if self.state == TCtrlState.cValDone:
                    self.expression = ""
                    self.state = TCtrlState.cEditing
                self.expression += cmd.upper()
                return self.expression
            # Точка доступна только в системах счисления с основанием больше 2
            elif cmd == "." and self.current_base > 2:
                if self.state == TCtrlState.cValDone:
                    self.expression = ""
                    self.state = TCtrlState.cEditing
                if "." not in self.expression:
                    self.expression += cmd
                return self.expression

            # Операции
            elif cmd in "+-*/^":
                if self.expression:
                    if self.first_number is None:
                        self.first_number = self.expression
                        self.last_operation = cmd
                        self.expression += cmd
                    else:
                        # Вычисляем предыдущую операцию
                        result = self._evaluate_expression(self.first_number + self.expression)
                        self.first_number = result
                        self.last_operation = cmd
                        self.expression = result + cmd
                return self.expression

            elif cmd == "AC":
                self.expression = ""
                return self.expression
            elif cmd == "CE":
                # Удаляем последнее введенное число
                # Ищем последний оператор или начало строки
                last_operator = max(
                    self.expression.rfind(op) for op in "+-*/.^"
                )
                if last_operator == -1:
                    self.expression = ""
                else:
                    self.expression = self.expression[:last_operator + 1]
                return self.expression
            elif cmd == "BS":
                self.expression = self.expression[:-1]
                return self.expression
            elif cmd == "=":
                # Определяем тип редактора и вычисляем выражение соответствующим образом
                try:
                    if isinstance(self.editor, FEditor):
                        result = self._eval_fraction_expression(self.expression)
                    elif isinstance(self.editor, CEditor):
                        result = self._eval_complex_expression(self.expression)
                    else:
                        # Для P-чисел конвертируем в десятичную систему для вычисления
                        expr = self.expression
                        if self.current_base != 10:
                            # Разбиваем выражение на числа и операторы
                            parts = []
                            current = ""
                            for c in expr:
                                if c in "+-*/.^":
                                    if current:
                                        parts.append(str(int(current, self.current_base)))
                                        current = ""
                                    parts.append(c)
                                else:
                                    current += c
                            if current:
                                parts.append(str(int(current, self.current_base)))
                            expr = ''.join(parts)
                        
                        result = str(eval(expr.replace('^', '**')))
                        
                        # Конвертируем результат обратно в текущую систему
                        if self.current_base != 10:
                            dec_value = int(float(result))
                            if self.current_base == 16:
                                result = hex(dec_value)[2:].upper()
                            elif self.current_base == 8:
                                result = oct(dec_value)[2:]
                            elif self.current_base == 2:
                                result = bin(dec_value)[2:]
                            else:
                                digits = []
                                n = dec_value
                                while n:
                                    digits.append("0123456789ABCDEF"[n % self.current_base])
                                    n //= self.current_base
                                result = ''.join(reversed(digits)) if digits else '0'
                        
                    self.expression = result
                    return result
                except Exception:
                    self.expression = ""
                    return "Error"
            elif cmd == "MS":
                # Запомнить текущее значение
                self.memory.store(self._get_current_number())
                return self.expression
            elif cmd == "MR":
                # Вставить из памяти
                mem_val = self.memory.value
                self.expression += mem_val
                return self.expression
            elif cmd == "MC":
                self.memory.clear()
                return self.expression
            elif cmd == "M+":
                self.memory.add(self._get_current_number())
                return self.expression
            else:
                return self.expression
        except Exception as e:
            self.expression = ""
            return str(e)

    def _eval_fraction_expression(self, expr: str):
        from calc_numbers.TANumber import TFrac
        import re
        # Разбиваем выражение на слагаемые с учетом знаков
        terms = re.findall(r'[+-]?\d+/\d+', expr.replace(' ', ''))
        result = TFrac(0, 1)
        for term in terms:
            frac = TFrac()
            frac.from_string(term)
            result = result.add(frac)
        return result.to_string()

    def _eval_complex_expression(self, expr: str):
        from calc_numbers.TANumber import TComp
        import re
        # Удаляем пробелы и нормализуем выражение
        expr = expr.replace(' ', '').replace('+-', '-').replace('--', '+')
        if expr and expr[0] not in '+-':
            expr = '+' + expr
        # Разбиваем на слагаемые вида [+|-]a[+|-]bi
        terms = re.findall(r'([+-][0-9.]+(?:[+-][0-9.]+i)?)', expr)
        result = TComp(0, 0)
        for term in terms:
            comp = TComp()
            # Убираем ведущий + для from_string
            if term.startswith('+'):
                term = term[1:]
            comp.from_string(term)
            result = result.add(comp)
        return result.to_string()

    def _get_current_number(self):
        # Получить текущее число для памяти
        if isinstance(self.editor, FEditor):
            from calc_numbers.TANumber import TFrac
            frac = TFrac()
            frac.from_string(self.expression)
            return frac
        elif isinstance(self.editor, CEditor):
            from calc_numbers.TANumber import TComp
            comp = TComp()
            comp.from_string(self.expression)
            return comp
        else:
            return TPNumber(float(self.expression) if self.expression else 0)

    def get_display(self) -> str:
        return self.expression

    def _process_operation(self, op: str):
        self.proc.lop = self._editor_to_number()
        self.proc.op = op
        self.editor.clear()
        return self.proc.lop.to_string()

    def _process_function(self, func: str):
        self.proc.right = self._editor_to_number()
        self.proc.func_run(func)
        return self.proc.right.to_string()

    def _process_equals(self):
        self.proc.right = self._editor_to_number()
        self.proc.op_run()
        self.editor.set_string = self.proc.lop.to_string()
        return self.proc.lop.to_string()

    def _editor_to_number(self):
        s = self.editor.get_string
        if isinstance(self.editor, PEditor):
            return TPNumber(float(s))
        elif isinstance(self.editor, FEditor):
            from calc_numbers.TANumber import TFrac
            frac = TFrac()
            frac.from_string(s)
            return frac
        elif isinstance(self.editor, CEditor):
            from calc_numbers.TANumber import TComp
            comp = TComp()
            comp.from_string(s)
            return comp
        else:
            return TPNumber(0) 