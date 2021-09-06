#<span style="color:red">Домашнее задание на Flask:</span
REST API (backend) для сайта объявлений.

## <span style="color:green">Возможности:</span>

### Класс пользователи
- создавать пользователя
- смотреть список пользователей (только для зарегенных)
- смотреть конкретного пользователя
- удалить пользователя (только зарегенный и только сам себя)

--- Пароли хэшированы md5

### Класс объявления
- список объявлений
- добавить объявление (только для зарегенных)
- изменить объявление (только для зарегенных и только своё)
- удалить объявление (только для зарегенных и только своё)

--- нельзя изменить автора сообщения методом patch

## <span style="color:blue">Описание</span>
* models.py - модели, пользователя и объявления
* views.py - вью-классы MethodView
* auth.py - функция-декоратор для проверки аутентификации
* app.py - подключение к БД postgres, создание приложения flask, миграции БД
* run.py - собственно запускающий файл
* http_requests.http - список всех запросов, которые тестировались