from flask import render_template, flash, redirect, url_for

from app.models import User

from . import bp
from app.forms import RegisterForm, SigninForm

@bp.route('/signin', methods=['GET',"POST"])
def signin():
    form = SigninForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            print(f'{form.username.data} signing in')
        else:
            print('user doesn\'t exist or incorrect password')

    return render_template('signin.jinja', form=form)

@bp.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        email = User.query.filter_by(email=form.email.data).first()
        if not email and not user:
            u = User(username=form.username.data,email=form.email.data)
            u.password = u.hash_password(form.password.data)
            u.commit()
            flash(f"{form.username.data} registered")
            return redirect(url_for("main.home"))
        if user:
            flash(f'{form.username.data} already taken, try again')
        else:
            flash(f'{form.email.data} already taken, try again')
    return render_template('register.jinja', form=form)