import flask_login
from flask import request, redirect, render_template, url_for, session, make_response, current_app
import routes
from __init__ import app
from flask_login import LoginManager
import database
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, UserMixin, current_user


login_manager = LoginManager(app)
login_manager.login_view = 'auth'
login_manager.login_message = 'Авторизуйтесь для доступа к ссылке'
login_manager.login_message_category = 'success'

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

class UserLogin(UserMixin):
    def fromDB(self, user_id, database):
        self.user = database.getUser(user_id)
        return self

    def create(self, user):
        self.user = user
        return self

    def get_id(self):
        session['user'] = self.user[0]
        return str(self.user[0])


@login_manager.user_loader
def load_user(user_id):
    return UserLogin().fromDB(user_id, database)


if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True)


