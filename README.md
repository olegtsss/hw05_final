# Cсылка на развернутый проект

https://yatube.git.olegtsss.ru:5002

### Описание проекта Yatube

Проект представляет собой социальную сеть для записей внезапных мыслей. 

### Используемые технологии

Python 3.7, Django 2.2, Django ORM, SQLite3, Paginator

### Как запустить проект:

- Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/olegtsss/hw05_final.git
cd hw05_final
```

- Cоздать и активировать виртуальное окружение:

```
python -m venv venv
. venv/Scripts/activate
```

- Обновить менеджер пакетов:

```
python -m pip install --upgrade pip
```

- Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

- Выполнить миграции:

```
python manage.py migrate
```

- Cоздать суперпользователя:

```
python manage.py createsuperuser
```

- Cобрать статику:

```
python manage.py collectstatic --no-input
```

- Запустить проект:

```
python manage.py runserver
```

### Разработчики

[olegtsss](https://github.com/olegtsss): backend
[yandex](https://ya.ru): frontend

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)
