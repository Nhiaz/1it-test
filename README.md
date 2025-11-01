# CashFlow — минимальный CRUD (Django + SQLite)

Учебный сервис учёта денежных операций (поступления / списания) со справочниками и базовой бизнес‑валидацией.

## Live-демо:
- Админ панель: https://1it.nhiaz.ru/admin (Логин: admin, Пароль: admin)
- Пользовательский UI: https://1it.nhiaz.ru/

---
## Сущности
**Справочники:**
- **Type** – тип операции (например: «Поступление», «Списание»)
- **Status** – статус операции (например: «План», «Факт»)
- **Category** – принадлежит конкретному Type
- **SubCategory** – принадлежит Category

**Операция `CashFlow`:**
Поля: `date`, `type` (FK), `status` (FK), `category` (FK), `subcategory` (FK, необяз.), `amount`, `comment`, `created_at`, `updated_at`

**Бизнес‑правила (реализованы в `CashFlow.clean()`):**
- `amount > 0`
- `category.type == type`
- если указана подкатегория: `subcategory.category == category`

---
## Возможности
- Создание / просмотр / редактирование / удаление операций через админку
- Фильтр и управление через стандартный интерфейс `/admin`
- Справочники расширяемые (можно добавлять новые Type / Status / Category / SubCategory)
- Idempotent команда заполнения стартовыми ссылочными данными

(Пользовательский отдельный кастомный UI минимум — опора на админ‑панель как на самый простой «junior» вариант.)

---
## Технологии
- Python >= 3.13 (соответствует `pyproject.toml`)
- Django 5.1.x
- SQLite (файл `db.sqlite3`)
- uv (менеджер зависимостей)

---
## Установка и запуск
1. Установите [uv](https://github.com/astral-sh/uv) (если ещё не установлен)
2. В корне проекта:

```bash
# Установить зависимости (создаст .venv согласно pyproject.toml)
uv sync
# Применить миграции
uv run manage.py migrate
# (Опционально) заполнить справочники демо-данными
uv run manage.py seed_refs
# (Опционально) создать суперпользователя для входа в админку
uv run manage.py createsuperuser
# Запуск сервера разработки
uv run manage.py runserver
```

Откройте:
- Админка: http://127.0.0.1:8000/admin/
- Пользовательский UI: http://127.0.0.1:8000/
> Примечание: Отдельный пользовательский интерфейс (витрина / формы вне админки) упрощён намеренно, чтобы сохранить минимализм тестового решения.

---
## Команда заполнения справочников
```bash
uv run manage.py seed_refs
```
Добавляет примеры типов, статусов, категорий и подкатегорий.

---
## Структура
```
project/                # Настройки Django
  settings.py
  urls.py
cashflow/               # Приложение
  models.py             # Type, Status, Category, SubCategory, CashFlow (+ clean())
  admin.py              # Регистрация и базовые списки
  views.py              # Минимальные представления
  urls.py               
  management/commands/seed_refs.py
templates/              # Шаблоны
  base.html
  cashflow/
    list.html
    form.html
```

---
## Валидация
Логика целостности вынесена в `CashFlow.clean()`, а метод `save()` вызывает `full_clean()` для гарантированной проверки при каждом сохранении.

---
## Возможные направления улучшений
- Добавить REST/JSON API (Django REST Framework)
- Пагинация и сортировка списка операций
- Тесты (валидация, команды, интеграционные)
- Отчёты / агрегаты (суммы по типам, периодам)
- Экспорт CSV / XLSX
- Dockerfile + docker-compose
- UI на HTMX/Alpine.js или React/Vue (при необходимости)

---
## Лицензия
MIT-License
