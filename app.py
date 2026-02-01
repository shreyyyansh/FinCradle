from flask import Flask
from config import SQLALCHEMY_DATABASE_URI, SECRET_KEY
from extensions import db, login, bcrypt, mail

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
    app.config["SECRET_KEY"] = SECRET_KEY
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.config.from_object("config")

    db.init_app(app)
    login.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)

    from routes.auth import auth
    from routes.finance import finance
    from routes.advisor import advisor

    app.register_blueprint(auth)
    app.register_blueprint(finance)
    app.register_blueprint(advisor)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
