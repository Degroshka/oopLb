import tkinter as tk
from tkinter import ttk, messagebox
from controllers.UControl import TCtrl

class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Universal Calculator")
        self.controller = TCtrl()
        
        # Минимальный размер окна
        self.root.minsize(500, 700)
        
        # Стили для виджетов
        style = ttk.Style()
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TButton', padding=10, font=('Arial', 12))
        style.configure('TLabel', font=('Arial', 12))
        style.configure('TRadiobutton', font=('Arial', 12))
        style.configure('TScale', background='#f0f0f0')
        
        # Основной фрейм
        self.main_frame = ttk.Frame(root, padding="20", style='TFrame')
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Настройка сетки
        for i in range(10):  # 10 строк
            self.main_frame.grid_rowconfigure(i, weight=1)
        for i in range(4):   # 4 столбца
            self.main_frame.grid_columnconfigure(i, weight=1)
        
        # Создаем словари с позициями кнопок
        self.create_buttons()
        
        # Кнопка справки слева
        help_btn = ttk.Button(self.main_frame, text="Справка", command=self.show_help, style='TButton')
        help_btn.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        
        # Поле ввода
        self.display = ttk.Entry(self.main_frame, justify="right", font=("Arial", 24))
        self.display.grid(row=1, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=10)
        self.display.insert(0, "0")
        self.display.config(state="readonly")
        
        # Фрейм для переключателей типа числа
        self.type_frame = ttk.Frame(self.main_frame, style='TFrame')
        self.type_frame.grid(row=2, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=10)
        
        # Переключатели типа числа
        self.number_type = tk.StringVar(value="P")
        ttk.Radiobutton(self.type_frame, text="P-число", variable=self.number_type, 
                       value="P", command=self.on_number_type_change).grid(row=0, column=0, padx=30)
        ttk.Radiobutton(self.type_frame, text="Дробь", variable=self.number_type, 
                       value="F", command=self.on_number_type_change).grid(row=0, column=1, padx=30)
        ttk.Radiobutton(self.type_frame, text="Комплексное", variable=self.number_type, 
                       value="C", command=self.on_number_type_change).grid(row=0, column=2, padx=30)

        # Фрейм для ползунка системы счисления
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

        # Создаем все кнопки
        self.create_memory_buttons()
        self.create_operation_buttons()
        self.create_number_buttons()
        self.create_control_buttons()

        # Привязка клавиш
        self.root.bind("<Key>", self.on_key_press)
        self.root.bind("<F1>", lambda e: self.show_help())

        # Инициализация начального состояния
        self.update_number_buttons_state(10)
        self.base_frame.grid()
    
    def on_number_type_change(self):
        """Handle number type change"""
        self.controller.set_number_type(self.number_type.get())
        self.controller.command("AC")  # Используем AC вместо C для очистки
        self.update_display()
        # Показываем ползунок только для P-чисел
        if self.number_type.get() == "P":
            self.base_frame.grid()
            self.update_number_buttons_state(self.base_var.get())
        else:
            self.base_frame.grid_remove()
            # Включаем все кнопки для дробей и комплексных
            self.update_number_buttons_state(16)
    
    def create_buttons(self):
        """Create calculator buttons"""
        # Memory buttons
        self.memory_buttons = {
            "MC": (4, 0), "MR": (4, 1), "MS": (4, 2), "M+": (4, 3)
        }
        
        # Operation buttons
        self.operation_buttons = {
            "+": (5, 3), "-": (6, 3), "*": (7, 3), "/": (8, 3),
            "^": (9, 3)
        }
        
        # Number buttons (A-F и C как цифра)
        self.number_buttons = {
            "7": (5, 0), "8": (5, 1), "9": (5, 2),
            "4": (6, 0), "5": (6, 1), "6": (6, 2),
            "1": (7, 0), "2": (7, 1), "3": (7, 2),
            "0": (8, 0), ".": (8, 1), "+/-": (8, 2),
            "A": (9, 0), "B": (9, 1), "C": (9, 2),
            "D": (10, 0), "E": (10, 1), "F": (10, 2)
        }
        
        # Control buttons (AC для очистки всего поля, CE для удаления последнего числа)
        self.control_buttons = {
            "AC": (9, 3), "CE": (10, 3), "BS": (8, 3), "=": (11, 3)
        }
    
    def create_memory_buttons(self):
        """Create memory operation buttons"""
        for text, pos in self.memory_buttons.items():
            btn = ttk.Button(self.main_frame, text=text, 
                           command=lambda t=text: self.on_button_click(t))
            btn.grid(row=pos[0], column=pos[1], padx=2, pady=2, sticky='nsew')
    
    def create_operation_buttons(self):
        """Create arithmetic operation buttons"""
        for text, pos in self.operation_buttons.items():
            btn = ttk.Button(self.main_frame, text=text, 
                           command=lambda t=text: self.on_button_click(t))
            btn.grid(row=pos[0], column=pos[1], padx=2, pady=2, sticky='nsew')
    
    def create_number_buttons(self):
        """Create number input buttons"""
        for text, pos in self.number_buttons.items():
            btn = tk.Button(self.main_frame, text=text, font=('Arial', 12),
                          command=lambda t=text: self.on_button_click(t),
                          bg='#e0e0e0', activebackground='#d0d0d0',
                          disabledforeground='#a0a0a0',
                          relief=tk.RAISED, borderwidth=2)
            btn.grid(row=pos[0], column=pos[1], padx=2, pady=2, sticky='nsew')
    
    def create_control_buttons(self):
        """Create control buttons"""
        for text, pos in self.control_buttons.items():
            btn = ttk.Button(self.main_frame, text=text, 
                           command=lambda t=text: self.on_button_click(t))
            btn.grid(row=pos[0], column=pos[1], padx=2, pady=2, sticky='nsew')
    
    def is_allowed_digit(self, char):
        base = self.base_var.get()
        allowed = "0123456789ABCDEF"[:base]
        return char.upper() in allowed

    def on_button_click(self, command):
        """Handle button clicks"""
        try:
            # Если это команда очистки
            if command in ["AC", "CE"]:
                self.controller.command(command)
                self.update_display()
                return

            # Если это точка, проверяем систему счисления
            if command == "." and self.base_var.get() <= 2:
                return

            # Если это цифра или буква
            if command in "0123456789ABCDEF":
                if not self.is_allowed_digit(command):
                    return
                current = self.controller.get_display()
                # Запрет незначащих нулей
                if current == "0" and command == "0":
                    return  # Не добавляем еще один ноль
                if current == "0" and command != ".":
                    self.controller.expression = ""  # Стираем ведущий ноль
                self.controller.command(command)
                self.update_display()
                return

            # Если это операция или равно
            if command in "+-*/^=":
                self.controller.command(command)
                self.update_display()
                return

            # Остальные команды
            self.controller.command(command)
            self.update_display()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def update_display(self):
        """Update calculator display"""
        try:
            self.display.config(state="normal")
            self.display.delete(0, tk.END)
            display_text = self.controller.get_display()
            self.display.insert(0, display_text)
            self.display.config(state="readonly")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def on_key_press(self, event):
        """Handle key presses"""
        try:
            key = event.char.upper()
            keysym = event.keysym.upper()
            
            # Проверяем буквы A-F
            if key in "ABCDEF":
                if not self.is_allowed_digit(key):
                    return
                current = self.controller.get_display()
                if current == "0":
                    self.controller.expression = ""
                self.controller.command(key)
                self.update_display()
                return

            # Проверяем цифры
            if key in "0123456789":
                if not self.is_allowed_digit(key):
                    return
                current = self.controller.get_display()
                if current == "0" and key == "0":
                    return
                if current == "0" and key != ".":
                    self.controller.expression = ""
                self.controller.command(key)
                self.update_display()
                return

            # Проверяем точку
            if key == "." and self.base_var.get() <= 2:
                return

            # Проверяем специальные клавиши
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
            messagebox.showerror("Error", str(e))

    def on_base_change(self, value):
        old_base = self.base_var.get()
        base = int(float(value))
        self.base_var.set(base)
        if hasattr(self, "base_value_label"):
            self.base_value_label.config(text=str(base))
        
        # Проверяем, существует ли number_buttons, если нет - создаем
        if not hasattr(self, "number_buttons"):
            self.create_buttons()
            self.create_number_buttons()
        
        # Обновляем состояние кнопок в зависимости от системы счисления
        allowed = "0123456789ABCDEF"[:base]
        for text, pos in self.number_buttons.items():
            for widget in self.main_frame.grid_slaves(row=pos[0], column=pos[1]):
                if isinstance(widget, tk.Button):
                    if text in allowed or not text.isalnum():
                        widget.config(state="normal")
                    else:
                        widget.config(state="disabled")
        
        # Конвертируем текущее значение в новую систему счисления
        current = self.display.get()
        try:
            if current and all(c.upper() in "0123456789ABCDEF"[:old_base] for c in current):
                # Конвертируем из старой системы в десятичную
                dec_value = int(current, old_base)
                # Конвертируем из десятичной в новую систему
                if base == 10:
                    new_str = str(dec_value)
                elif base == 16:
                    new_str = hex(dec_value)[2:].upper()
                elif base == 8:
                    new_str = oct(dec_value)[2:]
                elif base == 2:
                    new_str = bin(dec_value)[2:]
                else:
                    digits = []
                    n = dec_value
                    while n:
                        digits.append("0123456789ABCDEF"[n % base])
                        n //= base
                    new_str = ''.join(reversed(digits)) if digits else '0'
                
                # Обновляем отображение
                self.display.config(state="normal")
                self.display.delete(0, tk.END)
                self.display.insert(0, new_str)
                self.display.config(state="readonly")
                
                # Обновляем выражение в контроллере
                if hasattr(self.controller, "set_base"):
                    self.controller.set_base(base)
                    self.controller.expression = new_str  # Обновляем выражение напрямую
        except Exception as e:
            print(f"Error converting number: {e}")
            pass

    def update_number_buttons_state(self, base):
        """Обновляет состояние кнопок в зависимости от системы счисления"""
        allowed = "0123456789ABCDEF"[:base]
        for text, pos in self.number_buttons.items():
            for widget in self.main_frame.grid_slaves(row=pos[0], column=pos[1]):
                if isinstance(widget, tk.Button):
                    # Точка доступна только в системах счисления с основанием больше 2
                    if text == ".":
                        if base <= 2:
                            widget.config(state="disabled")
                            widget.config(bg='#cccccc')  # Делаем кнопку визуально неактивной
                        else:
                            widget.config(state="normal")
                            widget.config(bg='#e0e0e0')  # Возвращаем нормальный цвет
                    elif text in allowed or not text.isalnum():
                        widget.config(state="normal")
                        widget.config(bg='#e0e0e0')
                    else:
                        widget.config(state="disabled")
                        widget.config(bg='#cccccc')

    def show_help(self):
        # Проверяем, не открыто ли уже окно справки
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Toplevel) and widget.winfo_exists():
                widget.lift()  # Поднимаем существующее окно наверх
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
        help_window.geometry("600x550")  # Увеличил высоту окна
        help_window.transient(self.root)  # Делаем окно зависимым от главного
        help_window.grab_set()  # Делаем окно модальным
        
        # Фрейм для текста справки
        frame = ttk.Frame(help_window, style='TFrame')
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Скроллбар
        scrollbar = ttk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Текстовое поле
        text = tk.Text(frame, wrap=tk.WORD, yscrollcommand=scrollbar.set, 
                      font=('Arial', 12), bg='#f8f8f8')
        text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar.config(command=text.yview)
        
        # Вставляем текст справки
        text.insert(tk.END, help_text)
        text.config(state=tk.DISABLED)  # Делаем текст только для чтения
        
        # Кнопка закрытия
        ttk.Button(help_window, text="Закрыть", command=help_window.destroy).pack(pady=10)

        # Обработчик закрытия окна
        def on_closing():
            help_window.destroy()
        
        help_window.protocol("WM_DELETE_WINDOW", on_closing)

def main():
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main() 