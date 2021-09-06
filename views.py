from flask import jsonify, request, make_response
from flask.views import MethodView

from app import app
from models import Advertisement, User
from auth import auth_required


class UserView(MethodView):
    """вью для получения списка пользователей, создания и удаления пользователей"""

    @auth_required
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
        user.hash_password(request.json['password'])
        User.add(user)

        response = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
        }
        return jsonify(response)

    @auth_required
    def delete(self, user_id):
        """удалить по user_id, только авторизированный и только сам себя"""
        user = User.query.get(user_id)
        if request.authorization.username == user.username:
            User.delete(user)
            return jsonify({"status": 204})
        return make_response('Нельзя удалить другого пользователя кроме себя!', 401)


class AdvertisementView(MethodView):
    """вью для получения списка объявлений, создания, удаления и обновления объявлений"""

    def get(self):
        """получение списка всех объявлений"""
        advertisements = Advertisement.query.all()
        ads_list = []
        for ad in advertisements:
            ads_list.append(
                {
                    'id': ad.id,
                    'title': ad.title,
                    'description': ad.description,
                    'time_created': ad.time_created,
                    'user_id': ad.user_id
                }
            )
        return jsonify(ads_list)

    @auth_required
    def post(self):
        """создать объявление, только авторизованный"""
        ad = Advertisement(**request.json)
        Advertisement.add(ad)

        response = {
            'id': ad.id,
            'title': ad.title,
            'description': ad.description,
            'time_created': ad.time_created,
            'user_id': ad.user_id
        }
        return jsonify(response)

    @auth_required
    def delete(self, ad_id):
        """удалить объявление по его ad_id, вернуть статус 204"""
        ad = Advertisement.query.get(ad_id)
        if request.authorization.username == ad.user.username:
            Advertisement.delete(ad)
            return jsonify({"status": 204})
        return make_response('Нельзя удалить чужое объявление!', 401)

    @auth_required
    def patch(self, ad_id):
        """изменить объявление"""
        ad = Advertisement.query.get(ad_id)
        data = Advertisement(**request.json)
        if data.user_id:
            return make_response('Нельзя изменять автора сообщения!', 401)
        if request.authorization.username == ad.user.username:
            ad.update(ad, data)
            response = {
                'id': ad.id,
                'title': ad.title,
                'description': ad.description,
                'time_created': ad.time_created,
                'user_id': ad.user_id
            }
            return jsonify(response)
        return make_response('Нельзя редактировать чужое объявление!', 401)


ad_view = AdvertisementView.as_view('ad_api')
user_view = UserView.as_view('user_api')

app.add_url_rule('/ads/',
                 view_func=ad_view,
                 methods=['GET', 'POST', ])
app.add_url_rule('/ads/<ad_id>',
                 view_func=ad_view,
                 methods=['DELETE', 'PATCH', ])
app.add_url_rule('/users/',
                 view_func=user_view,
                 methods=['GET', ],
                 defaults={'user_id': None})
app.add_url_rule('/users/<user_id>',
                 view_func=user_view,
                 methods=['GET', 'DELETE', ])
app.add_url_rule('/users/',
                 view_func=user_view,
                 methods=['POST', ])
