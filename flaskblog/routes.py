import secrets
import os
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort, jsonify, json, make_response
from flaskblog.forms import RegistrationForm, LoginForm, UpdateForm, PostForm
from flaskblog.models import User, Post
from flaskblog import app, bcrypt, db
from flask_login import login_user, current_user, logout_user, login_required
import simplejson

def save_picture(form_pictures):
    random_hex = secrets.token_hex(32)
    _, f_ext = os.path.splitext(form_pictures.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profiles_pics', picture_fn)
    picture_remove = os.path.join(app.root_path, 'static/profiles_pics', current_user.image_file)
    output_size = (125, 125)
    i = Image.open(form_pictures)
    i.thumbnail(output_size)
    i.save(picture_path)
    if os.path.isfile(picture_remove) and _ != 'default.jpg':
        os.remove(picture_remove)
    return picture_fn

@app.route("/")
@app.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=2)
    return render_template('home.html', posts=posts)

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        print('teste')
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pwd)
        db.session.add(user)
        db.session.commit()
        flash(f'{form.username.data} Your account has been created! Your are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateForm()
    if form.validate_on_submit():
        if form.picture.data:
            current_user.image_file = save_picture(form.picture.data)
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been update!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename = 'profiles_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file= image_file, form=form)

from datetime import datetime

@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash(f'{current_user.username} your has been created', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', 
                            title='New Post',
                            form=form,
                            legend='New Post')

@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form= PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been update!', 'success')
        return redirect(url_for('post', post_id=post.id))
    form.title.data = post.title
    form.content.data = post.content
    return render_template('create_post.html',
                     title='Update Post',
                     form=form,
                     legend='Update Post')

@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been Deleted!', 'success')
    return redirect(url_for('home'))

@app.route("/")
@app.route("/user/<string:username>/post")
def user_post(username):
    # username = request.args.get('username', type=str)
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(author=user)\
                .order_by(Post.date_posted.desc())\
                .paginate(page=page, per_page=2)
    return render_template('user_post.html', posts=posts)

@app.route("/users", methods=['GET'])
def user_name():
    user = User.query.all()
    response = simplejson.dumps(user, for_json=True)
    return response

@app.route("/users/create", methods=['POST'])
def user_create():
    data = request.data
    print(data)
    return data

@app.route("/posts", methods=['GET'])
def user_posts():
    user = Post.query.all()
    response = make_response(simplejson.dumps(user, for_json=True), 200)
    return response

@app.route("/posts/<int:post_id>", methods=['GET'])
def user_post_id(post_id):
    user = Post.query.get_or_404(post_id)
    response = simplejson.dumps(user, for_json=True)
    return response

@app.route("/posts/create", methods=['POST'])
def user_posts_create():
    data = json.loads(request.data)
    print(data['title'], data['content'], data['user'])
    if data['title'] and data['content'] and data['user']:
        user = User.query.filter_by(email=data['user']).first()
        post = Post(title=data['title'], content=data['content'], author=user)
        db.session.add(post)
        db.session.commit()
        response = { 'message': 'Your Post has been created {}'.format(post.id) }
    else:
        response = { 'message': 'Please fill the requirement content and title' }
    return jsonify(response)

@app.route("/posts/update/<int:post_id>", methods=['POST'])
def user_post_update(post_id):
    post = Post.query.get_or_404(post_id)
    data = json.loads(request.data)
    if data['title'] and data['content']:
        post.title = data['title']
        post.content = data['content']
        db.session.commit()
        response = { 'message': 'Your Post has been update {}'.format(post.id) }
    else:
        response = { 'message': 'Please fill the requirement content and title' }
    return jsonify(response)

@app.route("/posts/delete/<int:post_id>", methods=['DELETE', 'POST'])
def user_post_delete(post_id):
    post = Post.query.get_or_404(post_id)
    if post.id:
        response = { 'message': 'Your Post has been deleted {}'.format(post.id) }
        db.session.delete(post)
        db.session.commit()
    return jsonify(response)


