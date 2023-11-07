from flask import request, redirect, render_template, url_for, session, flash, make_response
from werkzeug.security import generate_password_hash, check_password_hash
import database
import sqlite3, uuid, hashlib, random
from __init__ import app
from main import UserLogin
from flask_login import LoginManager, login_user, login_required, logout_user, current_user


menu = [
    {'name': 'Главная', 'url': '/index'},
    {'name': 'Вход', 'url': '/auth'},
    {'name': 'Регистрация', 'url': '/reg'}
]
# with app.app_context():
#     if session.get('user') is not None:
#         menu = [
#             {'name': 'Главная', 'url': '/index'},
#             {'name': 'Вход', 'url': '/auth'},
#             {'name': 'Регистрация', 'url': '/reg'}
#         ]
#     else:
#         menu = [
#             {'name': 'Главная', 'url': '/index'},
#             {'name': 'Профиль', 'url': '/profile'},
#         ]

flag = None


@app.route("/<short>", methods=['GET', 'POST'])
def link(short):
    res = database.checkLinks(short)
    if len(res) > 0:
        short = res[0][2]
        long = res[0][1]
        if res[0][3] == 1:
            database.updateCount(res[0][0], res[0][4])
            return redirect(long)
        elif res[0][3] == 2:
            database.updateCount(res[0][0], res[0][4])
            session['next'] = long
            session['access'] = 2
            return redirect(url_for('auth'))
        elif res[0][3] == 3:
            database.updateCount(res[0][0], res[0][4])
            session['next'] = long
            session['access'] = 3
            session['link_owner'] = res[0][5]
            return redirect(url_for('auth'))
    return 'Ссылка не существует'




@app.route("/index", methods=['GET', 'POST'])
def index():
    global flag
    if request.method == 'POST':
        long_link = request.form.get('long_link')
        short_link = request.form.get('short_link')
        if short_link == None:
            short_link = hashlib.md5(long_link.encode()).hexdigest()[:random.randint(8, 12)]
        level = request.form.get('level')
        if len(long_link) < 5:
            flash('Слишком короткая ссылка')
        id = current_user.get_id()
        res = database.addLinks(id, long_link, short_link, level)
        if res:
            return redirect(url_for('mylinks'))
        else:
            flash('Не удалось создать ссылку', 'error')
        return render_template('index.html', menu=menu, flag=flag)
    else:
        return render_template('index.html', menu=menu, flag=flag)

@app.route("/base")
def base():
    global flag
    return render_template('base.html', menu=menu, flag=flag)


@app.route("/reg", methods=['GET', 'POST'])
def reg():
    global flag

    if current_user.is_authenticated:
        return redirect(url_for('index'))
    flag = False

    if request.method == 'POST':
        login = request.form.get('name')
        pswrd = request.form.get('pass')
        if len(login) > 4 and len(pswrd) > 4:
            hash = generate_password_hash(pswrd)
            res = database.register(login, hash)
            if res:
                flash('Вы успешно зарегистрированы, теперь вам нужно войти в свой аккаунт', 'success')
                return redirect(url_for('index', flag=flag))
            else:
                flash('Пользователь с такими данными уже существует', 'error')
        else:
            flash('Слишком короткий логин или пароль')
        return render_template('reg.html', menu=menu, flag=flag)
    else:
        return render_template('reg.html', menu=menu, flag=flag)


@app.route("/auth", methods=['GET', 'POST'])
def auth():
    global flag
    global menu
    if current_user.is_authenticated:
        flag = True
        menu = [
            {'name': 'Главная', 'url': '/index'},
            {'name': 'Профиль', 'url': '/profile'}
        ]
        if session.get('next') is not None:
                long = session['next']
                session.pop('next')
                if session['access'] == 2:
                    return redirect(long)
                elif session['access'] == 3:
                    if session['link_owner'] == session['user']:
                        return redirect(long)
                    else:
                        return('Вам закрыт доступ к данной ссылке')
        return redirect(url_for('profile'))


    if request.method == 'POST':
        login = request.form.get('name')
        pswrd = request.form.get('pass')
        user = database.authorization(login, pswrd)
        if user != None:
            if session.get('next') is not None:
                    long = session['next']
                    session.pop('next')
                    if session['access'] == 2:
                        return redirect(long)
                    elif session['access'] == 3:
                        if session['link_owner'] == session['user']:
                            return redirect(long)
                        else:
                            return('Вам закрыт доступ к данной ссылке')            
            if len(user) > 1:
                userLogin = UserLogin().create(user)
                login_user(userLogin)
                flag = True
                return redirect(url_for('index'))

            return redirect(request.args.get('next') or url_for('index', flag=flag))
        else:
            flash('Данные введены неверно')
        return render_template('auth.html', menu=menu, flag=flag)
    else:
        return render_template('auth.html', menu=menu, flag=flag)


@app.route('/logout')
@login_required
def logout():
    global flag
    logout_user()
    session.pop('user', None)
    flag = False
    flash('Вы вышли из профиля')
    return redirect(url_for('auth', flag=flag))


@app.route('/profile')
@login_required
def profile():
    flag = True
    return render_template('profile.html', menu=menu, flag=flag)


@app.route('/mylinks', methods=['GET', 'POST'])
@login_required
def mylinks():
    global flag
    res = database.searchLinks(session['user'])
    access = database.getAccess()
    btn = request.form.get('btn')
    id = request.form.get('id')
    del_btn = request.form.get('del_btn')
    if del_btn == 'Yes':
        database.delLinks(id)
    if btn == 'Yes':
        session['id_link'] = id
        return redirect(url_for('editLink'))
    return render_template('mylinks.html', menu=menu, flag=flag, res=res, access=access)

@app.route("/editLink", methods=['GET', 'POST'])
@login_required
def editLink():
    global flag
    res = database.getLinks(session['id_link'])
    accesses = database.getAccess()
    id = res[0][0]
    long = res[0][1]
    short = res[0][2]
    access = res[0][3]

    if request.method == 'POST':
        long_link = request.form.get('long_link')
        short_link = request.form.get('short_link')
        level = request.form.get('level')
        database.UpdateLink(id, long_link, short_link, level)

    return render_template('editLink.html', menu=menu, flag=flag, long=long, short=short, access=access, accesses=accesses)

