from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from hashlib import md5


db = SQLAlchemy()


class BaseMixin:
    """общие операции для пользователей и объявлений, создать, удалить, изменить"""

    def add(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def update(self, data):
        """self - тут в смысле у себя, data - пришедшие данные"""
        if data.title:
            self.title = data.title
        if data.description:
            self.description = data.description
        if data.user_id:
            self.user_id = data.user_id
        db.session.commit()


class User(db.Model, BaseMixin):
    """модель, описывающая пользователей"""

    id = db.Column(db.INTEGER, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(128), unique=True, index=True)
    password = db.Column(db.String(128))

    def hash_password(self, raw_password: str):
        """хэшируем пароль, перед добавлением пользователя, вызывается во вью"""
        self.password = md5(raw_password.encode()).hexdigest()

    def check_password(self, raw_password: str):
        """проверяем пароль, возвращаем тру или фолс"""
        return self.password == md5(raw_password.encode()).hexdigest()


class Advertisement(db.Model, BaseMixin):
    """модель, описывающая объявления, FK на пользователя"""

    __tablename__ = 'advertisement'  # собственно без этого она всё равно так называется

    id = db.Column(db.INTEGER, primary_key=True)
    title = db.Column(db.String(50))
    description = db.Column(db.Text)
    time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())

    user_id = db.Column(db.INTEGER, db.ForeignKey('user.id'))
    user = db.relationship('User')
