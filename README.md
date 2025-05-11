# Universal Calculator

A Windows-style calculator application that supports calculations with real numbers, complex numbers, and fractions in different number systems.

## Features

- Three calculation modes:
  - Real Numbers
  - Complex Numbers
  - Fractions
- Support for different number bases:
  - Binary (base 2)
  - Octal (base 8)
  - Decimal (base 10)
  - Hexadecimal (base 16)
- Memory operations (M+, M-, MR)
- Modern dark theme interface
- Comprehensive help system

## Installation

1. Make sure you have Python 3.7+ installed on your system
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the calculator:
```bash
python calculator.py
```

### Real Numbers Mode
- Basic arithmetic operations (+, -, *, /)
- Support for different number bases
- Example: 1010 (binary) = 10 (decimal)

### Complex Numbers Mode
- Use 'i' for imaginary part
- Example: 2+3i
- Basic arithmetic operations

### Fractions Mode
- Use '/' for division
- Example: 1/2 + 1/3
- Results are displayed as fractions

### Memory Operations
- M+: Add current value to memory
- M-: Subtract current value from memory
- MR: Recall memory value

### Keyboard Shortcuts
- Enter: Calculate
- Escape: Clear

## Requirements

- Python 3.7+
- tkinter
- customtkinter

## License

This project is open source and available under the MIT License. 