from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, make_response
)

from werkzeug.security import generate_password_hash

from MUSQL.models import Account

import functools

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    from flask import current_app
    db = current_app.db
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            existing_user = Account.query.filter(
                Account.user_id == username).first()
            if existing_user is None:
                new_user = Account(user_id=username,
                                   password=generate_password_hash(password))
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for("auth.login"))
            else:
                error = f"User {username} is already registered."

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        account = Account.query.filter_by(user_id=username).first()

        if account is None:
            error = 'Incorrect username.'
        else:
            if not account.check_password(password):
                error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['loggedin'] = True
            session['id'] = account.id
            session['user_id'] = account.user_id
            resp = make_response(redirect(url_for('musql.home')))
            resp.set_cookie('session_id', value=str(session['id']).encode())

            return resp
        
        flash(error)

    return render_template('auth/login.html', error=error)


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('id')

    if user_id is None:
        g.user = None
    else:
        g.user = Account.query.filter(Account.id == user_id).first()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
