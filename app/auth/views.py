from app.models import User
from . import auth
from flask import render_template,redirect,url_for, flash,request
# from flask_login import login_user, logout_user, login_required
from .forms import RegistrationForm
from .. import db
from ..email import mail_message


@auth.route('/register',methods = ["GET","POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email = form.email.data, username = form.username.data,password = form.password.data)
        db.session.add(user)
        db.session.commit()

        mail_message("Welcome to Pitch Deck","email/welcome_user",user.email,user=user)
        return redirect(url_for('auth.login'))

    title = "SignUp | PitchDeck"
    return render_template('auth/register.html',registration_form = form,title = title)

