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
            # Преобразуем строку редактора в число
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

    def __del__(self):
        pass 