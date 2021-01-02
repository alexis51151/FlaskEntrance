from flask_sqlalchemy import SQLAlchemy  # database
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

db = SQLAlchemy()


class User(UserMixin, db.Model):
    email = db.Column(db.String(120), primary_key=True)
    password = db.Column(db.String(128))
    authenticated = db.Column(db.Boolean, default=False)

    def get_id(self):
        return self.email

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
