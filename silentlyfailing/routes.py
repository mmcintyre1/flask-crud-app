from flask import (
    Blueprint, Response, flash, g, redirect, render_template, request, url_for
)
from flask_login import login_required, login_user, logout_user, LoginManager, current_user

from .models import User, Post
from .forms import LoginForm

sf = Blueprint('sf', __name__)
login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    try:
        return User.query.get(user_id)
    except:
        return None


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash('You must be logged in to view that page.')
    return redirect(url_for('sf.login'))


@sf.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        print('hello')
        return redirect(url_for('sf.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user and user.check_password(password=form.password.data):
            login_user(user)
            flash('Logged in successfully.')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('sf.index'))

        flash('Invalid username/password combination')

        return redirect(url_for('sf.login'))

    return render_template('login.html', form=form)


@sf.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('sf.login')


@sf.route('/detail')
def detail():
    posts = Post.query.all()
    return render_template('detail.html', posts=posts)


@sf.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            post = Post(title=title, body=body)
            post.save_post()
            return redirect(url_for('sf.detail'))

    return render_template('create.html')


@sf.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            post.update_post(title, body)
            return redirect(url_for('sf.detail'))

    return render_template('update.html', post=post)


@sf.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    post = get_post(id)
    post.delete()
    return redirect(url_for('sf.detail'))


def get_post(id: int) -> Post:
    return Post.query.get_or_404(id)
