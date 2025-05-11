from enum import Enum
from editors.UAEditor import PEditor, FEditor, CEditor, AEditor
from processor.UProcssr import TProc
from memory.UMemory import TMemory
from calc_numbers.TANumber import TANumber, TPNumber, TFrac, TComp

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
        if not isinstance(self.editor, PEditor):
            raise ValueError("Только для P-чисел")
        if base < 2 or base > 16:
            raise ValueError("Основание от 2 до 16")
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
                # Убираем незначащие нули в начале числа
                if self.expression == "0":
                    self.expression = ""
                elif self.expression and self.expression[-1] in "+-*/^":
                    # Если последний символ - операция, добавляем пробел после неё
                    self.expression += " "
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
                # Если это дробный режим или комплексный режим и операция степени, игнорируем
                if (isinstance(self.editor, (FEditor, CEditor)) and cmd == "^"):
                    return self.expression

                if self.expression:
                    # Если это дробный режим и вводится /, проверяем, что это не операция деления
                    if isinstance(self.editor, FEditor) and cmd == "/":
                        # Проверяем, что последний символ не является операцией
                        if self.expression and self.expression[-1] not in "+-*/^":
                            self.expression += cmd
                            return self.expression
                    
                    # Если это дробный режим и вводится другая операция
                    if isinstance(self.editor, FEditor) and cmd != "/":
                        # Проверяем последнюю операцию
                        last_op = None
                        for op in "+-*/^":
                            pos = self.expression.rfind(op)
                            if pos > -1 and (last_op is None or pos > last_op[1]):
                                last_op = (op, pos)
                        
                        # Если последней операции не было или это не деление, добавляем знаменатель
                        if last_op is None or last_op[0] != "/":
                            # Находим последнее число
                            if last_op is None:
                                last_number = self.expression.strip()
                            else:
                                last_number = self.expression[last_op[1] + 1:].strip()
                            
                            # Если число не является дробью, добавляем знаменатель
                            if '/' not in last_number:
                                try:
                                    num = int(last_number)
                                    if last_op is None:
                                        self.expression = f"{num}/1"
                                    else:
                                        self.expression = self.expression[:last_op[1] + 1] + f" {num}/1"
                                except ValueError:
                                    pass
                    
                    # Если последний символ - операция, заменяем её
                    if self.expression and self.expression[-1] in "+-*/^":
                        self.expression = self.expression[:-1] + cmd
                    else:
                        # Добавляем пробел перед операцией
                        if not self.expression.endswith(" "):
                            self.expression += " "
                        self.expression += cmd
                return self.expression

            elif cmd == "AC":
                self.expression = ""
                self.first_number = None
                self.last_operation = None
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
                if self.expression:
                    self.expression = self.expression[:-1]
                return self.expression

            elif cmd == "+/-":
                if self.expression:
                    try:
                        # Получаем последнее число из выражения
                        parts = self.expression.split()
                        if not parts:
                            return self.expression
                            
                        last_number = parts[-1]
                        
                        # Если последний символ - операция, ничего не делаем
                        if last_number in "+-*/^":
                            return self.expression

                        # Если это комплексное число
                        if isinstance(self.editor, CEditor):
                            if 'i' in last_number:
                                # Если есть вещественная часть
                                if '+' in last_number or '-' in last_number[1:]:
                                    real, imag = last_number.split('+') if '+' in last_number else last_number.split('-')
                                    if '-' in last_number[1:]:
                                        real = '-' + real
                                    imag = imag.replace('i', '')
                                    parts[-1] = f"-{real}-{imag}i" if not real.startswith('-') else f"{real[1:]}-{imag}i"
                                else:
                                    # Если только мнимая часть
                                    imag = last_number.replace('i', '')
                                    parts[-1] = f"-{imag}i" if not imag.startswith('-') else f"{imag[1:]}i"
                                self.expression = " ".join(parts)
                                return self.expression

                        # Если это дробный режим и число не является дробью, преобразуем его
                        if isinstance(self.editor, FEditor) and '/' not in last_number:
                            try:
                                num = int(last_number)
                                last_number = f"{num}/1"
                            except ValueError:
                                pass
                            
                        # Если это дробь, меняем знак числителя
                        if '/' in last_number:
                            num, den = last_number.split('/')
                            if num.startswith('-'):
                                num = num[1:]
                            else:
                                num = '-' + num
                            parts[-1] = f"{num}/{den}"
                            self.expression = " ".join(parts)
                        else:
                            # Для обычных чисел
                            if self.current_base != 10:
                                dec_value = int(last_number, self.current_base)
                            else:
                                dec_value = float(last_number)
                                
                            # Меняем знак
                            dec_value = -dec_value
                            
                            # Конвертируем обратно в текущую систему
                            if self.current_base != 10:
                                if dec_value.is_integer():
                                    result_str = self._convert_to_base(int(dec_value), self.current_base)
                                else:
                                    result_str = str(dec_value)
                            else:
                                result_str = str(dec_value)
                            
                            # Заменяем последнее число на результат
                            parts[-1] = result_str
                            self.expression = " ".join(parts)
                            
                    except Exception as e:
                        print(f"Error changing sign: {e}")
                return self.expression

            elif cmd == "1/x":
                # Вычисление обратного числа
                if self.expression:
                    try:
                        # Получаем последнее число из выражения
                        parts = self.expression.split()
                        last_number = parts[-1] if parts else "0"

                        # Если это комплексное число
                        if isinstance(self.editor, CEditor):
                            if 'i' in last_number:
                                # Для комплексных чисел используем TComp
                                comp = TComp()
                                comp.from_string(last_number)
                                result = comp.inverse()
                                parts[-1] = result.to_string()
                                self.expression = " ".join(parts)
                                return self.expression

                        # Если это дробный режим и число не является дробью, преобразуем его
                        if isinstance(self.editor, FEditor):
                            if '/' not in last_number:
                                try:
                                    num = int(last_number)
                                    last_number = f"{num}/1"
                                except ValueError:
                                    pass
                            
                            # Создаем дробь и вычисляем обратное число
                            frac = TFrac()
                            frac.from_string(last_number)
                            result = frac.inverse()
                            parts[-1] = result.to_string()
                            self.expression = " ".join(parts)
                            return self.expression
                        else:
                            # Для обычных чисел
                            if self.current_base != 10:
                                dec_value = int(last_number, self.current_base)
                            else:
                                dec_value = float(last_number)
                                
                            # Проверяем на ноль
                            if dec_value == 0:
                                raise ValueError("Division by zero")
                                
                            # Вычисляем обратное число
                            inverse_value = 1.0 / dec_value
                            
                            # Конвертируем результат в текущую систему счисления
                            if self.current_base != 10:
                                # Для целых чисел
                                if inverse_value.is_integer():
                                    result_str = self._convert_to_base(int(inverse_value), self.current_base)
                                else:
                                    # Для дробных чисел показываем в десятичной системе
                                    result_str = f"{inverse_value:.10f}".rstrip('0').rstrip('.')
                            else:
                                # Для десятичной системы также ограничиваем количество знаков
                                result_str = f"{inverse_value:.10f}".rstrip('0').rstrip('.')
                            
                            # Заменяем последнее число на результат
                            if parts:
                                parts[-1] = result_str
                                self.expression = " ".join(parts)
                            else:
                                self.expression = result_str
                                
                    except ValueError as ve:
                        print(f"Error calculating inverse: {ve}")
                        self.expression = "Error: Division by zero"
                    except Exception as e:
                        print(f"Error calculating inverse: {e}")
                        self.expression = "Error"
                return self.expression

            elif cmd == "=":
                try:
                    if not self.expression:
                        return "0"

                    # Определяем тип редактора и вычисляем выражение соответствующим образом
                    if isinstance(self.editor, FEditor):
                        try:
                            result = self._eval_fraction_expression(self.expression)
                            self.expression = result
                            return result
                        except ValueError as e:
                            self.expression = f"Error: {str(e)}"
                            return self.expression
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
                                        # Убираем незначащие нули и префиксы
                                        current = current.lstrip('0bBxXoO') or '0'
                                        try:
                                            parts.append(str(int(current, self.current_base)))
                                        except ValueError:
                                            parts.append(current)
                                        current = ""
                                    parts.append(c)
                                else:
                                    current += c
                            if current:
                                # Убираем незначащие нули и префиксы
                                current = current.lstrip('0bBxXoO') or '0'
                                try:
                                    parts.append(str(int(current, self.current_base)))
                                except ValueError:
                                    parts.append(current)
                            expr = ''.join(parts)
                        
                        result = str(eval(expr.replace('^', '**')))
                        
                        # Конвертируем результат обратно в текущую систему
                        if self.current_base != 10:
                            try:
                                dec_value = float(result)
                                if dec_value.is_integer():
                                    dec_value = int(dec_value)
                                    if self.current_base == 16:
                                        result = hex(dec_value)[2:].upper()
                                    elif self.current_base == 8:
                                        result = oct(dec_value)[2:]
                                    elif self.current_base == 2:
                                        result = bin(dec_value)[2:]
                                    else:
                                        digits = []
                                        n = abs(dec_value)
                                        while n:
                                            digits.append("0123456789ABCDEF"[n % self.current_base])
                                            n //= self.current_base
                                        result = ''.join(reversed(digits)) if digits else '0'
                                        if dec_value < 0:
                                            result = '-' + result
                                else:
                                    # Для дробных чисел показываем в десятичной системе
                                    # с ограничением количества знаков после запятой
                                    result = f"{dec_value:.10f}".rstrip('0').rstrip('.')
                            except ValueError:
                                pass
                    
                    self.expression = result
                    return result
                except Exception as e:
                    self.expression = ""
                    return "Error"

            elif cmd == "MS":
                # Запомнить текущее значение
                if self.expression:
                    try:
                        # Получаем последнее число из выражения
                        parts = self.expression.split()
                        last_number = parts[-1] if parts else "0"
                        
                        # Создаем число соответствующего типа
                        if isinstance(self.editor, FEditor):
                            number = TFrac()
                            number.from_string(last_number)
                        elif isinstance(self.editor, CEditor):
                            number = TComp()
                            number.from_string(last_number)
                        else:
                            # Для P-чисел
                            if self.current_base != 10:
                                dec_value = int(last_number, self.current_base)
                            else:
                                dec_value = float(last_number)
                            number = TPNumber(dec_value)
                            
                        self.memory.store(number)
                    except Exception as e:
                        print(f"Error storing in memory: {e}")
                return self.expression

            elif cmd == "MR":
                # Вставить из памяти
                try:
                    mem_val = self.memory.value
                    if self.expression and self.expression[-1] in "+-*/^":
                        self.expression += " " + mem_val
                    else:
                        self.expression = mem_val
                except Exception as e:
                    print(f"Error retrieving from memory: {e}")
                return self.expression

            elif cmd == "MC":
                self.memory.clear()
                return self.expression

            elif cmd == "M+":
                # Добавить к значению в памяти
                if self.expression:
                    try:
                        # Получаем последнее число из выражения
                        parts = self.expression.split()
                        last_number = parts[-1] if parts else "0"
                        
                        # Создаем число соответствующего типа
                        if isinstance(self.editor, FEditor):
                            number = TFrac()
                            number.from_string(last_number)
                        elif isinstance(self.editor, CEditor):
                            number = TComp()
                            number.from_string(last_number)
                        else:
                            # Для P-чисел
                            if self.current_base != 10:
                                dec_value = int(last_number, self.current_base)
                            else:
                                dec_value = float(last_number)
                            number = TPNumber(dec_value)
                            
                        self.memory.add(number)
                    except Exception as e:
                        print(f"Error adding to memory: {e}")
                return self.expression

            # Добавление мнимой единицы для комплексных чисел
            elif cmd == "i" and isinstance(self.editor, CEditor):
                if self.state == TCtrlState.cValDone:
                    self.expression = ""
                    self.state = TCtrlState.cEditing
                if not self.expression.endswith("i"):
                    self.expression += "i"
                return self.expression

            else:
                return self.expression
        except Exception as e:
            self.expression = ""
            return str(e)

    def _convert_to_base(self, number: int, base: int) -> str:
        """Конвертирует число в указанную систему счисления"""
        if number == 0:
            return "0"
        digits = []
        n = abs(number)
        while n:
            digits.append("0123456789ABCDEF"[n % base])
            n //= base
        result = ''.join(reversed(digits))
        return "-" + result if number < 0 else result

    def _eval_fraction_expression(self, expr: str):
        import re
        
        try:
            # Разбиваем выражение на части (числа и операторы)
            parts = []
            current = ""
            for c in expr:
                if c in "+-*/^ ":
                    if current:
                        # Преобразуем число в дробь
                        try:
                            if "/" in current:
                                # Если это уже дробь
                                frac = TFrac()
                                frac.from_string(current)
                            else:
                                # Если это целое число, добавляем знаменатель 1
                                frac = TFrac(int(current), 1)
                            parts.append(frac)
                        except ValueError:
                            parts.append(current)
                        current = ""
                    if c != " ":  # Пропускаем пробелы
                        parts.append(c)
                else:
                    current += c
            
            # Обрабатываем последнее число
            if current:
                try:
                    if "/" in current:
                        frac = TFrac()
                        frac.from_string(current)
                    else:
                        frac = TFrac(int(current), 1)
                    parts.append(frac)
                except ValueError:
                    parts.append(current)
            
            # Вычисляем выражение
            result = TFrac(0, 1)
            current_op = None
            
            for part in parts:
                if isinstance(part, TFrac):
                    if current_op is None:
                        result = part
                    else:
                        try:
                            if current_op == "+":
                                result = result.add(part)
                            elif current_op == "-":
                                result = result.subtract(part)
                            elif current_op == "*":
                                result = result.multiply(part)
                            elif current_op == "/":
                                result = result.divide(part)
                            elif current_op == "^":
                                # Для степени преобразуем степень в целое число
                                try:
                                    power = int(part.to_string().split('/')[0])
                                    if power < 0:
                                        raise ValueError("Power must be non-negative")
                                    result = result.power(power)
                                except (ValueError, IndexError):
                                    raise ValueError("Power must be a non-negative integer")
                        except Exception as e:
                            raise ValueError(f"Error in operation {current_op}: {str(e)}")
                elif part in "+-*/^":
                    current_op = part
            
            return result.to_string()
        except Exception as e:
            raise ValueError(f"Error evaluating expression: {str(e)}")

    def _eval_complex_expression(self, expr: str):
        import re
        
        # Разбиваем выражение на части (числа и операторы)
        parts = []
        current = ""
        for c in expr:
            if c in "+-*/^ ":
                if current:
                    # Преобразуем в комплексное число
                    try:
                        if 'i' in current:
                            # Если это уже комплексное число
                            comp = TComp()
                            comp.from_string(current)
                        else:
                            # Если это вещественное число
                            comp = TComp(float(current), 0)
                        parts.append(comp)
                    except ValueError:
                        parts.append(current)
                    current = ""
                if c != " ":  # Пропускаем пробелы
                    parts.append(c)
            else:
                current += c
        
        # Обрабатываем последнее число
        if current:
            try:
                if 'i' in current:
                    comp = TComp()
                    comp.from_string(current)
                else:
                    comp = TComp(float(current), 0)
                parts.append(comp)
            except ValueError:
                parts.append(current)
        
        # Вычисляем выражение
        result = TComp(0, 0)
        current_op = None
        
        for part in parts:
            if isinstance(part, TComp):
                if current_op is None:
                    result = part
                else:
                    if current_op == "+":
                        result = result.add(part)
                    elif current_op == "-":
                        result = result.subtract(part)
                    elif current_op == "*":
                        result = result.multiply(part)
                    elif current_op == "/":
                        result = result.divide(part)
                    elif current_op == "^":
                        # Для степени преобразуем степень в целое число
                        try:
                            power = int(part.real)
                            result = result.power(power)
                        except (ValueError, AttributeError):
                            raise ValueError("Power must be an integer")
            elif part in "+-*/^":
                current_op = part
        
        return result.to_string()

    def _get_current_number(self):
        # Получить текущее число для памяти
        if isinstance(self.editor, FEditor):
            frac = TFrac()
            frac.from_string(self.expression)
            return frac
        elif isinstance(self.editor, CEditor):
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
            frac = TFrac()
            frac.from_string(s)
            return frac
        elif isinstance(self.editor, CEditor):
            comp = TComp()
            comp.from_string(s)
            return comp
        else:
            return TPNumber(0) 