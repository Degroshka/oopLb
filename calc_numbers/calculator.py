import tkinter as tk
from tkinter import ttk
from TANumber import TPNumber, TComp

class Calculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Calculator")
        self.window.geometry("400x600")
        
        # Переменная для хранения текущего числа
        self.current_number = None
        self.current_operation = None
        self.first_number = None
        self.is_p_number = True  # True для P-чисел, False для комплексных
        self.base = 10  # Текущая система счисления
        
        # Создаем и размещаем элементы интерфейса
        self.create_widgets()
        
    def create_widgets(self):
        # Поле ввода
        self.display = tk.Entry(self.window, font=('Arial', 20), justify='right')
        self.display.grid(row=0, column=0, columnspan=4, padx=5, pady=5, sticky='nsew')
        
        # Ползунок для выбора системы счисления
        self.base_frame = tk.Frame(self.window)
        self.base_frame.grid(row=1, column=0, columnspan=4, padx=5, pady=5, sticky='nsew')
        
        # Метка для системы счисления
        self.base_label = tk.Label(self.base_frame, text="Система счисления: 10")
        self.base_label.pack(side=tk.LEFT, padx=5)
        
        # Ползунок
        self.base_slider = ttk.Scale(self.base_frame, from_=2, to=16, orient='horizontal',
                                   command=self.on_base_change, length=200)
        self.base_slider.set(10)
        self.base_slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Кнопки цифр и операций
        self.create_digit_buttons()
        self.create_operation_buttons()
        
        # Кнопка переключения режима
        self.mode_button = tk.Button(self.window, text="P-числа", command=self.toggle_mode)
        self.mode_button.grid(row=6, column=0, columnspan=4, padx=5, pady=5, sticky='nsew')
        
        # Настройка весов строк и столбцов
        for i in range(7):
            self.window.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.window.grid_columnconfigure(i, weight=1)
    
    def create_digit_buttons(self):
        # Создаем кнопки цифр
        self.digit_buttons = {}
        digits = "0123456789ABCDEF"
        for i, digit in enumerate(digits):
            row = (i + 2) // 4
            col = i % 4
            btn = tk.Button(self.window, text=digit, command=lambda d=digit: self.add_digit(d))
            btn.grid(row=row, column=col, padx=2, pady=2, sticky='nsew')
            self.digit_buttons[digit] = btn
    
    def create_operation_buttons(self):
        # Кнопки операций
        operations = [
            ('+', lambda: self.set_operation('+')),
            ('-', lambda: self.set_operation('-')),
            ('*', lambda: self.set_operation('*')),
            ('/', lambda: self.set_operation('/')),
            ('x²', self.square),
            ('1/x', self.inverse),
            ('=', self.calculate),
            ('C', self.clear)
        ]
        
        for i, (text, command) in enumerate(operations):
            row = (i // 4) + 2
            col = i % 4
            btn = tk.Button(self.window, text=text, command=command)
            btn.grid(row=row, column=col, padx=2, pady=2, sticky='nsew')
    
    def on_base_change(self, value):
        """Обработчик изменения системы счисления"""
        self.base = int(float(value))
        self.base_label.config(text=f"Система счисления: {self.base}")
        self.update_digit_buttons()
    
    def update_digit_buttons(self):
        """Обновляет состояние кнопок цифр в зависимости от системы счисления"""
        allowed_digits = TPNumber.get_allowed_digits(self.base)
        for digit, button in self.digit_buttons.items():
            if digit in allowed_digits:
                button.config(state='normal')
            else:
                button.config(state='disabled')
    
    def toggle_mode(self):
        """Переключение между P-числами и комплексными числами"""
        self.is_p_number = not self.is_p_number
        self.mode_button.config(text="P-числа" if self.is_p_number else "Комплексные")
        self.clear()
        
        # Показываем/скрываем ползунок системы счисления
        if self.is_p_number:
            self.base_frame.grid()
            self.update_digit_buttons()
        else:
            self.base_frame.grid_remove()
            # Активируем все кнопки для комплексных чисел
            for button in self.digit_buttons.values():
                button.config(state='normal')
    
    def add_digit(self, digit):
        """Добавление цифры в поле ввода"""
        current = self.display.get()
        self.display.delete(0, tk.END)
        self.display.insert(0, current + digit)
    
    def set_operation(self, operation):
        """Установка операции"""
        if self.first_number is None:
            try:
                if self.is_p_number:
                    self.first_number = TPNumber(float(self.display.get()), self.base)
                else:
                    self.first_number = TComp(self.display.get())
                self.current_operation = operation
                self.display.delete(0, tk.END)
            except ValueError as e:
                self.display.delete(0, tk.END)
                self.display.insert(0, f"Error: {str(e)}")
    
    def calculate(self):
        """Выполнение операции"""
        if self.first_number is not None and self.current_operation is not None:
            try:
                if self.is_p_number:
                    second_number = TPNumber(float(self.display.get()), self.base)
                else:
                    second_number = TComp(self.display.get())
                
                if self.current_operation == '+':
                    result = self.first_number.add(second_number)
                elif self.current_operation == '-':
                    result = self.first_number.subtract(second_number)
                elif self.current_operation == '*':
                    result = self.first_number.multiply(second_number)
                elif self.current_operation == '/':
                    result = self.first_number.divide(second_number)
                
                self.display.delete(0, tk.END)
                self.display.insert(0, result.to_string())
                self.first_number = None
                self.current_operation = None
            except ValueError as e:
                self.display.delete(0, tk.END)
                self.display.insert(0, f"Error: {str(e)}")
    
    def square(self):
        """Возведение в квадрат"""
        try:
            if self.is_p_number:
                number = TPNumber(float(self.display.get()), self.base)
            else:
                number = TComp(self.display.get())
            result = number.square()
            self.display.delete(0, tk.END)
            self.display.insert(0, result.to_string())
        except ValueError as e:
            self.display.delete(0, tk.END)
            self.display.insert(0, f"Error: {str(e)}")
    
    def inverse(self):
        """Вычисление обратного числа"""
        try:
            if self.is_p_number:
                number = TPNumber(float(self.display.get()), self.base)
            else:
                number = TComp(self.display.get())
            result = number.inverse()
            self.display.delete(0, tk.END)
            self.display.insert(0, result.to_string())
        except ValueError as e:
            self.display.delete(0, tk.END)
            self.display.insert(0, f"Error: {str(e)}")
    
    def clear(self):
        """Очистка калькулятора"""
        self.display.delete(0, tk.END)
        self.first_number = None
        self.current_operation = None
    
    def run(self):
        """Запуск приложения"""
        self.window.mainloop()

if __name__ == "__main__":
    calc = Calculator()
    calc.run() 