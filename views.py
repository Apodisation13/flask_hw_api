from flask import jsonify, request
from flask.views import MethodView

from app import app
from models import User, Advertisement


# @app.route('/')
# def hello_world():  # put application's code here
#     return 'Hello World!'


class UserView(MethodView):
    """вью для получения списка пользователей, создания и удаления пользователей"""

    def get(self, user_id):
        """список всех пользователей, или только user_id"""
        if user_id:
            user = User.query.get(user_id)
            response = {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email
                    }
            return jsonify(response)

        users = User.query.all()
        user_list = []
        for user in users:
            user_list.append(
                {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email
                }
            )
        return jsonify(user_list)

    def post(self):
        """создать пользователя, вернуть данные пользователя"""
        user = User(**request.json)
        # user.set_password(request.json['password'])

        User.add(user)

        response = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "password": user.password
        }
        return jsonify(response)

    def delete(self, user_id):
        """удалить пользователя по его user_id, вернуть статус 204"""
        user = User.query.get(user_id)
        User.delete(user)
        return jsonify({"status": 204})


class AdvertisementView(MethodView):
    """вью для получения списка объявлений, создания и удаления объявлений"""

    def get(self):
        """получение списка всех объявлений"""
        advertisements = Advertisement.query.all()
        ads_list = []
        for ad in advertisements:
            ads_list.append(
                {
                    'id': ad.id,
                    'username': ad.title,
                    'email': ad.description,
                    'time_created': ad.time_created,
                    'user': ad.user_id
                }
            )
        return jsonify(ads_list)

    def post(self):
        """создать объявление"""
        user = User(**request.json)
        # user.set_password(request.json['password'])

        User.add(user)

        response = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "password": user.password
        }
        return jsonify(response)


user_view = UserView.as_view('user_api')
ad_view = AdvertisementView.as_view('ad_api')

app.add_url_rule('/users/',
                 view_func=user_view,
                 methods=['GET', ],
                 defaults={'user_id': None})
app.add_url_rule('/users/<user_id>',
                 view_func=user_view,
                 methods=['GET', 'DELETE'])

app.add_url_rule('/users/',
                 view_func=user_view,
                 methods=['POST', ])

app.add_url_rule('/ads/',
                 view_func=ad_view,
                 methods=['GET', ])
