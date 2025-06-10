chcp 65001
@echo off
cls

:: Переход в папку проекта
cd /d "%~dp0%"

echo [1/2] Запуск тестов...
python -m unittest test.py

:: Проверяем, успешен ли запуск тестов
if %errorlevel% neq 0 (
    echo Тесты провалены! Бот не запущен.
    exit /b 1
)

echo [2/2] Запуск бота...
python main.py
