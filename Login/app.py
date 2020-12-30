from flask import Flask, render_template, flash, redirect, url_for
from flask_login import LoginManager, login_required    # authentication
from forms import LoginForm, RegistrationForm # secure login form



# Imports from project files
from models import User, db

login_manager = LoginManager()


def create_app():
    # create a Flask app
    app = Flask(__name__)
    app.debug = True
    app.config['SECRET_KEY'] = 'amazing-secret-key:)'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

    # init user authentication system
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    # Return the pointer to the app just initialized
    return app

def setup_database(app):
    # init SQLAlchemy
    db.init_app(app)
    with app.app_context():
        db.create_all()

app = create_app()
setup_database(app)


@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)


"""All the routes are listed below."""

"""Login page"""
@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.get(form.email.data)
        if user:
            if user.check_password_hash(form.password.data):
                user.authenticated = True
                db.session.add(user)
                db.session.commit()
                flash('Logged in successfully.')
    return render_template('login.html', form=form)

"""Registration page"""
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        print("success")
        user = User(email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
