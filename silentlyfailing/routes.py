from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)
from flask_login import login_required, login_user, logout_user, current_user

from .models import User, Post
from .forms import LoginForm, PostForm
from silentlyfailing import login_manager


sf = Blueprint('sf', __name__)


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
        return redirect(url_for('sf.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user and user.check_password(password=form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('sf.index'))

        flash('Invalid username/password combination')

        return redirect(url_for('sf.login'))

    return render_template('login.html', form=form)


@sf.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('sf.index'))


@sf.route('/')
@sf.route("/index")
def index():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)


@sf.route('/create-post', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            print(form)
            post = Post(title=form.title.data,
                        body=form.body.data.strip(),
                        author=form.author.data)
            post.save()
            return redirect(url_for('sf.index'))

    return render_template('create_post.html', form=form)


@sf.route('/<slug>/update-post', methods=('GET', 'POST'))
@login_required
def update_post(slug):
    post = get_post(slug)
    form = PostForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            title = form.title.data
            body = form.body.data.strip()
            post.update(title, body)
            return redirect(url_for('sf.index'))

    return render_template('update_post.html', form=form, post=post)


@sf.route('/<slug>/delete-post', methods=('POST',))
@login_required
def delete_post(slug):
    post = get_post(slug)
    post.delete()
    return redirect(url_for('sf.index'))


@sf.route("/<slug>")
def post_detail(slug):
    post = get_post(slug)
    return render_template('post_detail.html', post=post)


def get_post(slug: str) -> Post:
    return Post.query.filter_by(slug=slug).first()
