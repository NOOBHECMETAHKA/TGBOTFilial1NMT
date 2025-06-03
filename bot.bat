chcp 65001
@echo off
cls

:: Переход в папку проекта
cd /d "%~dp0%"

:: Активация виртуального окружения (если есть)
:: call venv\Scripts\activate

echo [1/3] Установка зависимостей...
pip install -r requirements.txt

echo [2/3] Запуск тестов...
python -m unittest test.py

:: Проверяем, успешен ли запуск тестов
if %errorlevel% neq 0 (
    echo Тесты провалены! Бот не запущен.
    exit /b 1
)

echo [3/3] Запуск бота...
python main.py
