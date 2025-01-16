# Cсылка на развернутый проект

https://yatube.git.olegtsss.ru

# Описание проекта Yatube:

Социальная сеть, позволяет зарегистрированным пользователям создавать записи на различные темы, комментировать сообщения, подписываться и отписываться от авторов. Включает панель администрирования: управление пользователями, создание, редактирование, удаление постов, объединение записей по тегам и пагинацию. Для хранение данных используется `SQLite`. Применен паттерн проектирования `MVC` (Model-View-Controller).

### Используемые технологии:

Python 3.7, Django 2.2

### Как запустить проект:

```
git clone https://github.com/olegtsss/hw05_final.git
cd hw05_final
python -m venv venv
. venv/Scripts/activate
python -m pip install --upgrade pip
pip install -r requirements.txt

python3 yatube/manage.py collectstatic
python3 yatube/manage.py createsuperuser
python3 yatube/manage.py runserver
```

### Разработчик:
[olegtsss](https://github.com/olegtsss)

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=whte)
