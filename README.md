Запуск проекта:

1) Клонировать репозиторий
```
git clone <url>
cd test_app
```

2) Создать виртуальное окружение (python3.12.3)
```
python3 -m venv .venv
```

3) Устанавливаем зависимости
```
pip install -r requirements.txt
cd test_app
```


4) Если нужно, создаем тестовые объекты в БД
```
python3 manage.py generate_menu_test_data
```

5) Запускаем сервер
```
python3 manage.py runserver
```


