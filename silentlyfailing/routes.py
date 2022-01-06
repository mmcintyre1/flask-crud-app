import flask
from flask_login import login_required, login_user, logout_user, LoginManager, current_user

from .models import User
from .forms import LoginForm

sf = flask.Blueprint('sf', __name__)
login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    try:
        return User.query.get(user_id)
    except:
        return None


@sf.route('/login', methods=['GET', 'POST'])
def login():
    print(current_user.is_authenticated)
    if current_user.is_authenticated:
        print('hello')
        return flask.redirect(flask.url_for('sf.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user and user.check_password(password=form.password.data):
            login_user(user)
            flask.flash('Logged in successfully.')
            next_page = flask.request.args.get('next')
            return flask.redirect(next_page or flask.url_for('sf.index'))

        flask.flash('Invalid username/password combination')

        return flask.redirect(flask.url_for('sf.login'))

    return flask.render_template('login.html', form=form)


@sf.route("/logout")
@login_required
def logout():
    logout_user()
    return flask.redirect('sf.login')


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flask.flash('You must be logged in to view that page.')
    return flask.redirect(flask.url_for('sf.login'))


@sf.route('/index')
@login_required
def index():
    return flask.Response("Hello World!")
