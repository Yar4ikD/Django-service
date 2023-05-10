# Friends - Django-сервис друзей.
Сервис написан для Web - пользования, и отдельно написан REST API.


## Начало работы
### Основные шаги для запуска работы:
1. Создайте виртуальное окружения
2. Установить зависимости с файла [requirements.txt](/requirements.txt)
3. Запустите утилиту командной строки Django для создания таблиц
4. Запустите веб-сервер.
```
venv\Scripts\activate.bat - для Windows;
source venv/bin/activate - для Linux и MacOS.
```
```
pip install -r requirements.txt
```
```
python manage.py makemigrations
python manage.py migrate
```
```
python manage.py runserver 
```

## Структура проекта бота 
- Корень проекта friends
- Приложения account (Модели и представления работы Web сервиса)
- Приложения apiaccount (Модели и представления работы API сервиса)
- Приложения authuser (Модели и представления для работы с объектом User (Web))
- db.sqlite3 (База данных)
- requirements.txt (Библиотеки)


## Работа сервиса и вызовы его API

### Регистрация 
- Чтобы работать с сервисом пользователь должен быть зарегистрирован и (или) пройти аутентификацию.

Регистрация пользователя происходит с помощью библиотеки djoser
- http://127.0.0.1:8000/api/register/users/

<img src="screenshots/Снимок экрана от 2023-05-10 19-37-51.png" width="500">

#### Просмотр списка друзей
- http://127.0.0.1:8000/api/friends/

Представления и сериализатор которые отвечают за работу endpoint:

```python
class FriendApiView(generics.ListAPIView):
class FriendSerializer(serializers.ModelSerializer):
```

#### Удаление пользователя из списка друзей.
- http://127.0.0.1:8000/api/friend/<int:pk>/delete/

- При удалении пользователем 1 из списка друзей пользователя 2, автоматически удаляются записи дружбы
у пользователя 1 и у пользователя 2.

Представления и сериализатор которые отвечают за работу endpoint:

```python
class DeleteFriendApiView(generics.DestroyAPIView):
class FriendSerializer(serializers.ModelSerializer):
```

### Просмотр всех зарегистрированных пользователей на сервисе

- http://127.0.0.1:8000/api/all-people/


- Вернется ответ - список пользователей с именем и ID, чтобы взаимодействовать с пользователями на сервесе нужно знать,
их имена и ID. 
Также, отправить запрос, на добавления в друзья, можно только тем пользователям которые зарегистрированные.


Представления и сериализатор которые отвечают за работу endpoint:

```python
class AllRegisterPeopleApiView(generics.ListAPIView):
class UserProfileSerializer(serializers.ModelSerializer):
```
<img src="screenshots/Снимок экрана от 2023-05-10 19-35-38.png" width="500">

### Отправка запроса в друзья и просмотр списка своих отправленных запросов:
- http://127.0.0.1:8000/api/sent-request/

- При отправке запроса в друзья, создаются записи в 2-х пользователей, отправителя и получателя.
- При отправке заявки в друзья укапается имя и ID пользователя, которому адресуется заявка.
- Если при отправке заявке пользователю, который ранее отправлял ранее заявку вам, 
запись заявки отправителя не создается и запись заявки отправленной другим пользователе ранее удаляются.
Создаются записи о дружбе у пользователей указанных ранее.

Представления и сериализатор которые отвечают за работу endpoint:

```python
class SentRequestApiView(generics.ListCreateAPIView):
class SentRequestSerializer(serializers.ModelSerializer):
```

<img src="screenshots/Снимок экрана от 2023-05-10 19-42-08.png" width="500">
<img src="screenshots/Снимок экрана от 2023-05-10 19-42-24.png" width="500">


### Просмотр входных заявок в друзья, подтверждение или отклонения заявки:

Просмотр списка заявок:
- http://127.0.0.1:8000/api/incoming-requests/

Подтверждения заявки:
- http://127.0.0.1:8000/api/<int:pk>/accept/

Отклонение заявки:
- http://127.0.0.1:8000/api/<int:pk>/delete/

pk - номер заявки.

- Пользователь видит заявки на добавления в друзья. 
- При подтверждении - записи заявки удаляются у пользователей и добавляются записи о дружбе.
- При отклонении - записи заявки удаляются.

Представления и сериализатор которые отвечают за работу endpoint:

```python
class IncomingRequestApiView(generics.ListAPIView): - просмотр
class AcceptRequestApiView(APIView): - подтверждения
class DeleteIncomingRequestApiView(generics.DestroyAPIView): - отклонение

class IncomingRequestSerializer(serializers.ModelSerializer):
```

### Получить информацию о статусе дружбы.
- http://127.0.0.1:8000/api/get-status/<int:friend_pk>/

pk - pk модели пользователя User

- Возвращается один из 4-х вариантов ответа

Представления и сериализатор которые отвечают за работу endpoint:

```python
class GetStatusApiView(APIView):
```
