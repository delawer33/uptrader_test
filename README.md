### Запуск проекта:

1) Клонировать репозиторий
```
git clone https://github.com/delawer33/uptrader_test
cd uptrader_test
```

2) Создать виртуальное окружение (python3.12.3)
```
python3 -m venv .venv
```

3) Устанавливаем зависимости
```
pip install -r requirements.txt
```

4) Переходим в приложение
```
cd test_app
```

5) Применяем миграции
```
python3 manage.py makemigrations
python3 manage.py migrate
```

6) Если нужно, создаем тестовые объекты в БД
```
python3 manage.py generate_menu_test_data
```

7) Запускаем сервер
```
python3 manage.py runserver
```

### Через docker-compose

```
sudo docker compose up --build
```
Если нужно запустить проет с postgres, можно в `docker-compose.yaml` раскомментировать сревис `db` и в `test_app/test_app/settings.py` раскомментировать настройку `DATABASES` с postgres. 

### Тесты

В `test_app/menu/tests` есть тесты для приложения `menu`, запуск:

```
python3 manage.py test menu
```
