import os
import sys
import unittest

# Добавляем корневую директорию проекта в путь поиска Python
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Загружаем все тесты
loader = unittest.TestLoader()
start_dir = os.path.join(os.path.dirname(__file__), 'tests')
suite = loader.discover(start_dir, pattern='test_*.py')

# Запускаем тесты
runner = unittest.TextTestRunner(verbosity=2)
runner.run(suite) 