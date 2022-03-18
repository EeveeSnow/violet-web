"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import Flask, make_response, redirect, render_template, request, session
from werkzeug.exceptions import HTTPException
from violet_main import app
from violet_main.data.users import User
from violet_main.data import db_session
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from violet_main.forms.RegisterForm import RegisterForm
from violet_main.forms.LoginForm import LoginForm


db_session.global_init("violet_main/db/IDE.db")
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)

@app.route('/')
@app.route('/news')
def home():
    """Renders the home page."""
    param = {}
    param["user"] = current_user.username
    return render_template(
        'index.html', param=param
        )

@app.route('/profile')
def profile():
    if current_user.is_authenticated:
        return render_template('profile.html')
    else:
        return redirect('/login')



@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )

#ERRORS PAGES
@app.errorhandler(418)
@app.route('/teapot')
def teapot():
    """Renders the teapot error page."""
    return render_template(
        'errors/teapot.html',
        title='Teapot'
    )

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('errors/404.html', title="404"), 404

@app.errorhandler(500)
def error500(e):
    """Renders the 500 error page."""
    return render_template(
        'errors/500.html',
        title='500'
    )

@app.route("/main")
def main():
    if current_user.is_authenticated:
        return redirect('/')
    else:
        return redirect('/login')


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Registration',
                                   form=form,
                                   message="Passwords not the same")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Registration',
                                   form=form,
                                   message="Whoops we already have some one with this name(")
        user = User(
            username=form.name.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Registration', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Wrong login or password",
                               form=form)
    return render_template('login.html', title='Autorisation', form=form)