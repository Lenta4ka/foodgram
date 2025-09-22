Foodgram – Продуктовый помощник

Foodgram — это веб-сервис, позволяющий пользователям публиковать рецепты, добавлять рецепты в избранное. Кроме того, можно скачать список продуктов, необходимых для приготовления блюда, просмотреть рецепты друзей и добавить любимые рецепты в список избранных.

Установка и запуск:
1. Клонируйте репозиторий: git clone https://github.com/lenta4ka/foodgram.git

2. Создайте .env файл с настройками: DB_ENGINE=django.db.backends.postgresql DB_NAME=postgres POSTGRES_USER=postgres POSTGRES_PASSWORD=postgres DB_HOST=food_db DB_PORT=5432 SECRET_KEY=ключ приложения django
ALLOWED_HOSTS=разрешенные хосты(your.domain.com,IP)

3.  Запустить Docker compose - sudo docker compose -f docker-compose.production.yml up -d

4. Примените миграции, соберите статику, создайте суперпользователя: docker compose exec backend python manage.py migrate docker compose exec backend python manage.py collectstatic --noinput docker compose exec backend python manage.py createsuperuser

5. На сервере настроить и запустить Nginx. Внесите изменения sudo nano /etc/nginx/sites-enabled/default и перезагрузите конфигурацию


Загрузка данных из фикстуры в папке data - docker-compose exec backend python manage.py load_ingredients ingredients.json

Пример доступных запросов:
Регистрация нового пользователя-.../api/users/
Получение всех рецептов, создать новый рецепт-.../api/recipes/
Список всех тегов-.../api/tags/

Адрес сайта: 84.201.137.106

Логин и пароль суперпользователя:

username: lenta
email: lenta4ka2010@mail.ru
password: lenta

