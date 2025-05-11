import PyInstaller.__main__
import os

# Получаем текущую директорию
current_dir = os.path.dirname(os.path.abspath(__file__))

# Пути к файлам
main_script = os.path.join(current_dir, 'main.py')
icon_path = os.path.join(current_dir, 'icon.ico')  # Если есть иконка

# Параметры сборки
params = [
    main_script,
    '--onefile',  # Создать один exe файл
    '--noconsole',  # Без консольного окна
    '--name=Calculator',  # Имя выходного файла
    '--clean',  # Очистить кэш перед сборкой
    '--add-data=README.md;.',  # Добавить README.md
]

# Добавить иконку, если она есть
if os.path.exists(icon_path):
    params.append(f'--icon={icon_path}')

# Запустить сборку
PyInstaller.__main__.run(params) 