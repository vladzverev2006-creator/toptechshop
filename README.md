# TopTechShop

Маркетплейс цифровых товаров (шаблоны, UI‑киты, плагины, пресеты).

## Домен
`https://toptechshop.isgood.host` (IP: `37.128.206.242`)

## Запуск локально
1. Установить зависимости:
   - `python3 -m pip install -r requirements.txt`
2. Скопировать `.env.example` в `.env` и задать значения.
3. Миграции:
   - `python3 manage.py migrate`
4. Создать суперпользователя:
   - `python3 manage.py createsuperuser`
5. Запуск:
   - `python3 manage.py runserver`

## Статика
- `python3 manage.py collectstatic`

## Логи
- Django лог: `/var/log/toptechshop/django.log`
- Nginx лог: `/var/log/nginx/toptechshop.error.log`

## Перезапуск сервиса
- `systemctl restart toptechshop-gunicorn`
- `systemctl restart nginx`

## Резервное копирование
- Ежедневный дамп БД: `pg_dump toptechshop > backup.sql`

## API
Примеры:
- `GET /api/products/?search=ui&limit=5`
- `GET /api/products/1/`
- `POST /api/products/` (требуется авторизация)

## Примечания
- DEBUG должен быть `0` на проде.
- Почтовые письма для восстановления пароля выводятся в консоль (EMAIL_BACKEND).
 - Тестовый пользователь: `demo` / `demo12345`
