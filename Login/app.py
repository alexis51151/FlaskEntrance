from flask import Flask, render_template, flash, redirect, url_for
from flask_login import LoginManager, login_required, login_user  # authentication
from forms import LoginForm, RegistrationForm  # secure login form
from flask_debugtoolbar import DebugToolbarExtension  # for debug

# Imports from project files
from models import User, db

login_manager = LoginManager()
toolbar = DebugToolbarExtension()


def create_app():
    # create a Flask app
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'amazing-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # init user authentication system
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    # init debug toolbar
    toolbar.init_app(app)

    # init the database
    db.init_app(app)
    with app.app_context():
        db.create_all()

    return app


app = create_app()


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
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            user.authenticated = True
            login_user(user)
            flash('Logged in successfully.')
            return redirect("google.com")
    return render_template('login.html', form=form)


"""Registration page"""


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data)
        user.set_password(form.password.data)
        print(user)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


if __name__ == '__main__':
    app.run()
