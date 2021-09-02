# from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func


db = SQLAlchemy()
# migrate = Migrate(app, db)


class User(db.Model):

    id = db.Column(db.INTEGER, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(128), unique=True, index=True)
    password = db.Column(db.String(30))

    def add(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Advertisement(db.Model):

    __tablename__ = 'advertisement'

    id = db.Column(db.INTEGER, primary_key=True)
    title = db.Column(db.String(50))
    description = db.Column(db.Text)
    time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())

    user_id = db.Column(db.INTEGER, db.ForeignKey('user.id'))
    user = db.relationship('User')
