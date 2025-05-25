import tkinter as tk
from tkinter import ttk, messagebox
from controllers.UControl import TCtrl

class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        self.controller = TCtrl()
        
        # мин. размер окна
        self.root.minsize(500, 700)
        
        # стили для виджетов
        style = ttk.Style()
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TButton', padding=10, font=('Arial', 12))
        style.configure('TLabel', font=('Arial', 12))
        style.configure('TRadiobutton', font=('Arial', 12))
        style.configure('TScale', background='#f0f0f0')
        
        # осн. фрейм
        self.main_frame = ttk.Frame(root, padding="20", style='TFrame')
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # настройка сетки
        for i in range(10):  # 10 строк
            self.main_frame.grid_rowconfigure(i, weight=1)
        for i in range(4):   # 4 столбца
            self.main_frame.grid_columnconfigure(i, weight=1)
        
        # словари с позициями кнопок
        self.create_buttons()
        
        # кнопка справки слева
        help_btn = ttk.Button(self.main_frame, text="Справка", command=self.show_help, style='TButton')
        help_btn.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        
        # поле ввода
        self.display = ttk.Entry(self.main_frame, justify="right", font=("Arial", 24))
        self.display.grid(row=1, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=10)
        self.display.insert(0, "0")
        self.display.config(state="readonly")
        
        # фрейм для переключателей типа числа
        self.type_frame = ttk.Frame(self.main_frame, style='TFrame')
        self.type_frame.grid(row=2, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=10)
        
        # переключатели типа числа
        self.number_type = tk.StringVar(value="P")
        ttk.Radiobutton(self.type_frame, text="P-число", variable=self.number_type, 
                       value="P", command=self.on_number_type_change).grid(row=0, column=0, padx=30)
        ttk.Radiobutton(self.type_frame, text="Дробь", variable=self.number_type, 
                       value="F", command=self.on_number_type_change).grid(row=0, column=1, padx=30)
        ttk.Radiobutton(self.type_frame, text="Комплексное", variable=self.number_type, 
                       value="C", command=self.on_number_type_change).grid(row=0, column=2, padx=30)

        # фрейм для ползунка системы счисления
        self.base_var = tk.IntVar(value=10)
        self.base_frame = ttk.Frame(self.main_frame, style='TFrame')
        self.base_frame.grid(row=3, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=10)
        self.base_label = ttk.Label(self.base_frame, text="Система счисления:", style='TLabel')
        self.base_label.pack(side=tk.LEFT, padx=5)
        self.base_slider = ttk.Scale(self.base_frame, from_=2, to=16, orient='horizontal',
                                    command=self.on_base_change, length=200)
        self.base_slider.set(10)
        self.base_slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.base_value_label = ttk.Label(self.base_frame, text="10", style='TLabel')
        self.base_value_label.pack(side=tk.LEFT, padx=5)

        # создаем все кнопки
        self.create_memory_buttons()
        self.create_operation_buttons()
        self.create_number_buttons()
        self.create_control_buttons()

        # привязка клавиш
        self.root.bind("<Key>", self.on_key_press)
        self.root.bind("<F1>", lambda e: self.show_help())

        # инициализация нач. состояния
        self.update_number_buttons_state(10)
        self.base_frame.grid()
    
    def on_number_type_change(self):
        """Обработка изменения типа числа"""
        self.controller.set_number_type(self.number_type.get())
        self.controller.command("AC")  # используем AC вместо C для очистки
        self.update_display()
        # показываем ползунок только для P-чисел
        if self.number_type.get() == "P":
            self.base_frame.grid()
            self.update_number_buttons_state(self.base_var.get())
            # Включаем кнопку степени для P-чисел
            for text, pos in self.operation_buttons.items():
                if text == '^':
                    for widget in self.main_frame.grid_slaves(row=pos[0], column=pos[1]):
                        if isinstance(widget, ttk.Button):
                            widget.config(state="normal")
                            widget.configure(style='TButton')
        else:
            self.base_frame.grid_remove()
            # отключаем буквы A-F для дробей и комплексных чисел
            for text, pos in self.number_buttons.items():
                for widget in self.main_frame.grid_slaves(row=pos[0], column=pos[1]):
                    if isinstance(widget, tk.Button):
                        if text in "ABCDEF":
                            widget.config(state="disabled")
                            widget.config(bg='#cccccc')  # делаем кнопку визуально неактивной
                            widget.config(disabledforeground='#999999')  # делаем текст серым
                        elif text in "0123456789.":
                            widget.config(state="normal")
                            widget.config(bg='#e0e0e0')  # возвращаем нормальный цвет
                            widget.config(disabledforeground='black')  # возвращаем нормальный цвет текста
                        elif text == "i":
                            # активируем кнопку i только для комплексных чисел
                            if self.number_type.get() == "C":
                                widget.config(state="normal")
                                widget.config(bg='#e0e0e0')
                                widget.config(disabledforeground='black')
                            else:
                                widget.config(state="disabled")
                                widget.config(bg='#cccccc')
                                widget.config(disabledforeground='#999999')

            # отключаем кнопку степени для дробных и комплексных чисел
            for text, pos in self.operation_buttons.items():
                if text == '^':
                    for widget in self.main_frame.grid_slaves(row=pos[0], column=pos[1]):
                        if isinstance(widget, ttk.Button):
                            widget.config(state="disabled")
                            widget.configure(style='Disabled.TButton')
    
    def create_buttons(self):
        """Создание кнопок калькулятора"""
        # кнопки памяти
        self.memory_buttons = {
            "MC": (4, 0), "MR": (4, 1), "MS": (4, 2), "M+": (4, 3)
        }
        
        # кнопки операций
        self.operation_buttons = {
            "+": (5, 3), "-": (6, 3), "*": (7, 3), "/": (8, 3),
            "^": (9, 3), "1/x": (10, 3)
        }
        
        # кнопки цифр (A-F и C как цифра)
        self.number_buttons = {
            "7": (5, 0), "8": (5, 1), "9": (5, 2),
            "4": (6, 0), "5": (6, 1), "6": (6, 2),
            "1": (7, 0), "2": (7, 1), "3": (7, 2),
            "0": (8, 0), ".": (8, 1), "+/-": (8, 2),
            "A": (9, 0), "B": (9, 1), "C": (9, 2),
            "D": (10, 0), "E": (10, 1), "F": (10, 2),
            "i": (11, 0)  # кнопка мнимой единицы
        }
        
        # кнопки управления (AC для очистки всего поля, CE для удаления последнего числа)
        self.control_buttons = {
            "AC": (11, 1), "CE": (11, 2), "BS": (11, 3), "=": (12, 3)
        }
    
    def create_memory_buttons(self):
        """Создание кнопок памяти"""
        for text, pos in self.memory_buttons.items():
            btn = ttk.Button(self.main_frame, text=text, 
                           command=lambda t=text: self.on_button_click(t))
            btn.grid(row=pos[0], column=pos[1], padx=2, pady=2, sticky='nsew')
    
    def create_operation_buttons(self):
        """Создание кнопок операций"""
        for text, pos in self.operation_buttons.items():
            btn = ttk.Button(self.main_frame, text=text, 
                           command=lambda t=text: self.on_button_click(t))
            btn.grid(row=pos[0], column=pos[1], padx=2, pady=2, sticky='nsew')
            # отключаем кнопку степени для дробных и комплексных чисел
            if text == '^':
                if self.number_type.get() in ["F", "C"]:
                    btn.config(state="disabled")
                    btn.configure(style='Disabled.TButton')

    def create_number_buttons(self):
        """Создание кнопок цифр"""
        for text, pos in self.number_buttons.items():
            btn = tk.Button(self.main_frame, text=text, font=('Arial', 12),
                          command=lambda t=text: self.on_button_click(t),
                          bg='#e0e0e0', activebackground='#d0d0d0',
                          disabledforeground='#a0a0a0',
                          relief=tk.RAISED, borderwidth=2)
            btn.grid(row=pos[0], column=pos[1], padx=2, pady=2, sticky='nsew')
    
    def create_control_buttons(self):
        """Создание кнопок управления"""
        for text, pos in self.control_buttons.items():
            btn = ttk.Button(self.main_frame, text=text, 
                           command=lambda t=text: self.on_button_click(t))
            btn.grid(row=pos[0], column=pos[1], padx=2, pady=2, sticky='nsew')
    
    def is_allowed_digit(self, char):
        base = self.base_var.get()
        allowed = "0123456789ABCDEF"[:base]
        return char.upper() in allowed

    def on_button_click(self, command):
        """Обработка нажатия кнопок"""
        try:
            # если это команда очистки
            if command in ["AC", "CE"]:
                self.controller.command(command)
                self.update_display()
                return

            # если это точка, проверяем систему счисления
            if command == "." and self.base_var.get() <= 2:
                return

            # если это цифра или буква
            if command in "0123456789ABCDEF":
                if not self.is_allowed_digit(command):
                    return
                self.controller.command(command)
                self.update_display()
                return

            # если это операция или равно
            if command in "+-*/^=" or command == "1/x":
                # для операции степени в режиме P-чисел
                if command == "^" and self.number_type.get() == "P":
                    # получаем текущее выражение
                    expr = self.display.get()
                    if expr:
                        try:
                            # разбиваем на число и степень
                            parts = expr.split("^")
                            if len(parts) == 2:
                                base = float(parts[0])
                                power = float(parts[1])
                                result = base ** power
                                # конвертируем результат в текущую систему счисления
                                if self.base_var.get() != 10:
                                    if result.is_integer():
                                        result = int(result)
                                        result_str = self._convert_to_base(result, self.base_var.get())
                                    else:
                                        # для дробных чисел показываем в десятичной системе
                                        result_str = f"{result:.10f}".rstrip('0').rstrip('.')
                                else:
                                    result_str = f"{result:.10f}".rstrip('0').rstrip('.')
                                self.display.config(state="normal")
                                self.display.delete(0, tk.END)
                                self.display.insert(0, result_str)
                                self.display.config(state="readonly")
                                return
                        except Exception as e:
                            print(f"Ошибка вычисления степени: {e}")
                
                self.controller.command(command)
                self.update_display()
                return

            # остальные команды
            self.controller.command(command)
            self.update_display()
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))
    
    def update_display(self):
        """Обновление дисплея"""
        try:
            self.display.config(state="normal")
            self.display.delete(0, tk.END)
            display_text = self.controller.get_display()
            self.display.insert(0, display_text)
            self.display.config(state="readonly")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))
    
    def on_key_press(self, event):
        """Обработка нажатия клавиш"""
        try:
            key = event.char.upper()
            keysym = event.keysym.upper()
            
            # проверяем буквы A-F
            if key in "ABCDEF":
                if not self.is_allowed_digit(key):
                    return
                self.controller.command(key)
                self.update_display()
                return

            # проверяем цифры
            if key in "0123456789":
                if not self.is_allowed_digit(key):
                    return
                self.controller.command(key)
                self.update_display()
                return

            # проверяем точку
            if key == "." and self.base_var.get() <= 2:
                return

            # проверяем специальные клавиши
            if event.keysym == "Return":
                self.controller.command("=")
                self.update_display()
            elif event.keysym == "BackSpace":
                self.controller.command("BS")
                self.update_display()
            elif key in ".+-*/^":
                self.controller.command(key)
                self.update_display()
            elif key == ",":
                self.controller.command(".")
                self.update_display()
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def on_base_change(self, value):
        old_base = self.base_var.get()
        base = int(float(value))
        self.base_var.set(base)
        if hasattr(self, "base_value_label"):
            self.base_value_label.config(text=str(base))
        
        # обновляем состояние кнопок в зависимости от системы счисления
        allowed = "0123456789ABCDEF"[:base]
        for text, pos in self.number_buttons.items():
            for widget in self.main_frame.grid_slaves(row=pos[0], column=pos[1]):
                if isinstance(widget, tk.Button):
                    if text in allowed or not text.isalnum():
                        widget.config(state="normal")
                        widget.config(bg='#e0e0e0')
                        widget.config(disabledforeground='black')
                    else:
                        widget.config(state="disabled")
                        widget.config(bg='#cccccc')
                        widget.config(disabledforeground='#999999')
        
        # конвертируем текущее значение в новую систему счисления
        current = self.display.get()
        try:
            if current:
                # разбиваем выражение на части (числа и операторы)
                parts = []
                current_part = ""
                for c in current:
                    if c in "+-*/^ ":
                        if current_part:
                            # удаляем префиксы систем счисления
                            current_part = current_part.lstrip('bBxXoO')
                            
                            # конвертируем число из старой системы в десятичную
                            try:
                                if "." in current_part:
                                    # для дробных чисел берем только целую часть
                                    integer_part = current_part.split(".")[0]
                                    dec_value = int(integer_part, old_base)
                                else:
                                    # для целых чисел
                                    dec_value = int(current_part, old_base)
                                
                                # конвертируем из десятичной в новую систему
                                if base == 10:
                                    # для десятичной системы показываем как есть
                                    new_str = str(dec_value)
                                else:
                                    # для не-десятичных систем используем новый метод конвертации
                                    new_str = self._convert_to_base(dec_value, base)
                                
                                parts.append(new_str)
                            except ValueError:
                                # если не удалось конвертировать, оставляем как есть
                                parts.append(current_part)
                            current_part = ""
                        parts.append(c)
                    else:
                        current_part += c
                
                # обрабатываем последнюю часть
                if current_part:
                    try:
                        # удаляем префиксы систем счисления
                        current_part = current_part.lstrip('bBxXoO')
                        
                        if "." in current_part:
                            # для дробных чисел берем только целую часть
                            integer_part = current_part.split(".")[0]
                            dec_value = int(integer_part, old_base)
                        else:
                            # для целых чисел
                            dec_value = int(current_part, old_base)
                        
                        # конвертируем из десятичной в новую систему
                        if base == 10:
                            # для десятичной системы показываем как есть
                            new_str = str(dec_value)
                        else:
                            # для не-десятичных систем используем новый метод конвертации
                            new_str = self._convert_to_base(dec_value, base)
                        
                        parts.append(new_str)
                    except ValueError:
                        parts.append(current_part)
                
                # собираем новое выражение
                new_expression = ''.join(parts)
                
                # обновляем отображение
                self.display.config(state="normal")
                self.display.delete(0, tk.END)
                self.display.insert(0, new_expression)
                self.display.config(state="readonly")
                
                # обновляем выражение в контроллере
                if hasattr(self.controller, "set_base"):
                    self.controller.set_base(base)
                    self.controller.expression = new_expression
        except Exception as e:
            print(f"Ошибка конвертации числа: {e}")
            pass

    def update_number_buttons_state(self, base):
        """Обновление состояния кнопок в зависимости от системы счисления"""
        allowed = "0123456789ABCDEF"[:base]
        for text, pos in self.number_buttons.items():
            for widget in self.main_frame.grid_slaves(row=pos[0], column=pos[1]):
                if isinstance(widget, tk.Button):
                    # точка доступна только в системах счисления с основанием больше 2
                    if text == ".":
                        if base <= 2:
                            widget.config(state="disabled")
                            widget.config(bg='#cccccc')  # делаем кнопку визуально неактивной
                            widget.config(disabledforeground='#999999')  # делаем текст серым
                        else:
                            widget.config(state="normal")
                            widget.config(bg='#e0e0e0')  # возвращаем нормальный цвет
                            widget.config(disabledforeground='black')  # возвращаем нормальный цвет текста
                    elif text in allowed or not text.isalnum():
                        widget.config(state="normal")
                        widget.config(bg='#e0e0e0')
                    else:
                        widget.config(state="disabled")
                        widget.config(bg='#cccccc')

    def show_help(self):
        # проверяем, не открыто ли уже окно справки
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Toplevel) and widget.winfo_exists():
                widget.lift()  # поднимаем существующее окно наверх
                return

        help_text = """
Универсальный калькулятор

Типы чисел:
- P-число: числа в различных системах счисления (2-16)
- Дробь: обыкновенные дроби
- Комплексное: комплексные числа

Основные операции:
+ : сложение
- : вычитание
* : умножение
/ : деление
^ : возведение в степень

Управление:
AC : очистка всего поля
CE : удаление последнего введенного числа
BS : удаление последнего символа
= : вычисление результата

Память:
MS : сохранить число в память
MR : вставить число из памяти
MC : очистить память
M+ : добавить к числу в памяти

Системы счисления (для P-чисел):
- Используйте ползунок для выбора системы (2-16)
- Доступные цифры: 0-9, A-F (в зависимости от системы)

Горячие клавиши:
F1 : открыть справку
Enter : вычисление (=)
Backspace : удаление последнего символа (BS)
"""
        help_window = tk.Toplevel(self.root)
        help_window.title("Справка")
        help_window.geometry("600x550")  # увеличил высоту окна
        help_window.transient(self.root)  # делаем окно зависимым от главного
        help_window.grab_set()  # делаем окно модальным
        
        # фрейм для текста справки
        frame = ttk.Frame(help_window, style='TFrame')
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # скроллбар
        scrollbar = ttk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # текстовое поле
        text = tk.Text(frame, wrap=tk.WORD, yscrollcommand=scrollbar.set, 
                      font=('Arial', 12), bg='#f8f8f8')
        text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar.config(command=text.yview)
        
        # вставляем текст справки
        text.insert(tk.END, help_text)
        text.config(state=tk.DISABLED)  # делаем текст только для чтения
        
        # кнопка закрытия
        ttk.Button(help_window, text="Закрыть", command=help_window.destroy).pack(pady=10)

        # обработчик закрытия окна
        def on_closing():
            help_window.destroy()
        
        help_window.protocol("WM_DELETE_WINDOW", on_closing)

    def _convert_to_base(self, number: float, base: int) -> str:
        """Конвертация числа в указанную систему счисления"""
        if number == 0:
            return "0"
            
        # обработка отрицательных чисел
        is_negative = number < 0
        number = abs(number)
        
        # берем только целую часть
        integer_part = int(number)
        
        # конвертируем целую часть
        if integer_part == 0:
            integer_str = "0"
        else:
            digits = []
            n = integer_part
            while n:
                digits.append("0123456789ABCDEF"[n % base])
                n //= base
            integer_str = ''.join(reversed(digits))
        
        # собираем результат
        result = integer_str
        return "-" + result if is_negative else result

def main():
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main() 