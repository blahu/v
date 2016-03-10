from flask import render_template, current_app, request, redirect, url_for, \
    flash
from flask.ext.login import login_user, logout_user, login_required
from .. import db
from ..models import Vets
from . import auth
from .forms import LoginForm
from datetime import datetime 


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if not current_app.config['DEBUG'] and not current_app.config['TESTING'] \
            and not request.is_secure:
        return redirect(url_for('.login', _external=True, _scheme='https'))

    form = LoginForm()

    if form.validate_on_submit():
        vet = Vets.query.filter_by(login_name=form.login.data).first()

        if vet is None:
            flash('Invalid login name or password.')
            return redirect(url_for('.login'))
        else:
            pw_checked = vet.verify_password(form.password.data) 
            if not pw_checked:
               # set last failed login
               vet.last_failed_login = datetime.utcnow() 
               db.session.add(vet)
               db.session.commit()
             
	       lash('Invalid login name or password.')
               return redirect(url_for('.login'))

        # login successful
        login_user(vet, form.remember_me.data)

        # set last good login
        vet.last_good_login = datetime.utcnow() 
        db.session.add(vet)
        db.session.commit()

        return redirect(request.args.get('next') or url_for('index'))

    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('index'))
