# Makefile — удобные команды для разработки

.PHONY: check test format cov install

# Полная проверка: стиль + формат + тесты + покрытие
check:
	ruff check . --fix
	black .
	pytest --cov --cov-fail-under=80

# Запуск тестов
test:
	pytest -v

# Форматирование кода
format:
	black .
	ruff check . --fix

# Отчёт о покрытии в браузере
cov:
	pytest --cov --cov-report=html
	@echo "Открой htmlcov/index.html в браузере"

# Установка проекта в режиме разработки
install:
	pip install -e .[dev]

# Очистка временных файлов
clean:
	@rm -rf htmlcov/ .pytest_cache/ __pycache__/ *.pyc
	@echo "Временные файлы удалены"
