from functools import wraps

from flask import request, make_response

from models import User


def auth_required(f):
    """ищем пользователя по username, проверяем голый пароль"""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth:
            return make_response('НЕОБХОДИМА АУТЕНТИФИКАЦИЯ!', 401)

        user = User.query.filter_by(username=auth.username).first()
        if not user:
            return make_response('Такого пользователя нет!', 401)
        if not user.check_password(raw_password=auth.password):
            return make_response('Неверный пароль!', 401)

        return f(*args, **kwargs)

    return decorated
