@echo off
:: Устанавливаем UTF-8
chcp 65001 > nul

:: Цвета
set green=[92m
set yellow=[93m
set red=[91m
set reset=[0m

:: Показываем, какую команду запустили
if "%~1" == "" goto help
if "%~1" == "install" goto install
if "%~1" == "test" goto test
if "%~1" == "format" goto format
if "%~1" == "check" goto check
if "%~1" == "cov" goto cov
if "%~1" == "clean" goto clean

:: Если команда не найдена
echo.%red%Ошибка:%reset% команда "%~1" не найдена.
echo.
goto help_usage

:: ============== Метки ==============
:install
echo.%green%Устанавливаю зависимости...%reset%
pip install -e .[dev]
exit /b %errorlevel%

:test
echo.%green%Запускаю тесты...%reset%
pytest -v
exit /b %errorlevel%

:format
echo.%green%Форматирую код...%reset%
black . && ruff check . --fix
exit /b %errorlevel%

:check
echo.%green%Полная проверка...%reset%
black . && ruff check . --fix && pytest --cov --cov-fail-under=80
exit /b %errorlevel%

:cov
echo.%green%Запускаю тесты и создаю отчёт...%reset%
pytest --cov --cov-report=html
echo.%yellow%Открываю отчёт в браузере...%reset%
start "" "htmlcov\index.html"
exit /b %errorlevel%

:clean
echo.%yellow%Очищаю временные файлы...%reset%
rmdir /s /q htmlcov .pytest_cache __pycache__ 2>nul
del /q *.pyc *.pyo *.pyd 2>nul
echo.%green%Готово. Временные файлы удалены.%reset%
exit /b 0

:help
echo.
echo Использование: make ^<команда^>
echo.
echo   %green%make install%reset%   Установить зависимости 
echo   %green%make format%reset%    Отформатировать код
echo   %green%make test%reset%      Запустить тесты
echo   %green%make check%reset%     Полная проверка
echo   %green%make cov%reset%       Покрытие тестами (отчёт в браузере)
echo   %green%make clean%reset%     Удалить временные файлы
echo.
exit /b 0

:help_usage
echo   make install   Установить зависимости
echo   make format    Отформатировать код
echo   make test      Запустить тесты
echo   make check     Полная проверка
echo   make cov       Покрытие тестами (отчёт в браузере)
echo   make clean     Удалить временные файлы
echo.
exit /b 1
