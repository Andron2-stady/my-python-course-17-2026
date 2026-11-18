# Тесты для YouGile API

Набор позитивных и негативных тестов для проверки эндпоинтов POST, PUT и GET.

## Установка

1. Склонируйте репозиторий.
2. Создайте виртуальное окружение.
   python -m venv venv
   source venv/bin/activate  # или venv\Scripts\activate на Windows

## Настройка ключа

1. Скопируйте шаблон:
   bash
   cp .env.example .env
2. Получите API-ключ: https://ru.yougile.com/api-v2#/operations/AuthKeyController_create
   (нужны логин, пароль и companyId(копируется в интерфейсе по Ctrl+Alt+Q / Ctrl+Option+Q).)
3. Впишите значения в .env:
   YOUGILE_BASE_URL=https://ru.yougile.com/api-v2
   YOUGILE_API_KEY=<ваш ключ>

## Запуск

`bash
pytest -v                       - все тесты
pytest tests/test_projects_positive.py -v
pytest -v -k "create"            - по имени