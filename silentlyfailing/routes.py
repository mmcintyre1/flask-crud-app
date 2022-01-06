import flask
from flask_login import login_required, login_user, logout_user, LoginManager

from .models import User
from .forms import LoginForm

sf = flask.Blueprint('sf', __name__)
login_manager = LoginManager()


@sf.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(password=form.password.data):
            flask.flash('Logged in successfully.')
            login_user(user)
            next_page = flask.request.args.get('next')
            return flask.redirect(next_page or flask.url_for('sf.index'))
        flask.flash('Invalid username/password combination')
        return flask.redirect(flask.url_for('sf.login'))
    return flask.render_template('login.html', form=form)


@sf.route("/logout")
@login_required
def logout():
    logout_user()
    return flask.redirect('/')


@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in on every page load."""
    if user_id is not None:
        return User.query.get(user_id)
    return None


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flask.flash('You must be logged in to view that page.')
    return flask.redirect(flask.url_for('login.html'))


@sf.route('/index')
def index():
    return flask.Response("Hello World!")
