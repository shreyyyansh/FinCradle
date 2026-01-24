from extensions import db, login
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def get_id(self):
        return str(self.user_id)


@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
