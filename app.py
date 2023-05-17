from flask import Flask, render_template, redirect, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'supersecret'

toolbar = DebugToolbarExtension(app)

app.app_context().push()

connect_db(app)
db.create_all()


"""User routes"""

@app.route('/')
def root():
    return redirect('/users')

@app.route('/users')
def users_index():
    """show list of all users in db"""

    users = User.query.order_by(User.last_name, User.first_name).all()

    return render_template('index.html', users= users)

@app.route('/users/new')
def show_new_user():
    """show new user page"""

    return render_template('new.html')

@app.route('/users/new', methods=["POST"])
def upload_new_user():
    """send new user data to db"""

    new_user = User(first_name= request.form['first_name'],
                    last_name= request.form['last_name'],
                    image_url= request.form['image_url'] or None)
    
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>')
def show_user_info(user_id):
    """show user information"""

    user = User.query.get(user_id)
    return render_template('profile.html', user=user)

@app.route('/users/<int:user_id>/edit')
def edit_info(user_id):
    """show user edit page"""

    user = User.query.get(user_id)
    return render_template('edit-user.html', user= user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def handle_info(user_id):
    """update db with new data"""
    
    user = User.query.get(user_id)

    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def handle_delete_user(user_id):
    """remove a user from the db"""

    user= User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users') 

################################################################

"""Post routes"""

@app.route('/user/<int:user_id>/posts/new')
def show_new_post_form(user_id):
    """display new post page"""

    user = User.query.get(user_id)
    return render_template('add-post.html', user = user)

@app.route('/user/<int:user_id>/posts/new', methods=["POST"])
def handle_new_post(user_id):
    """send post data to db"""

    user= User.query.get(user_id)

    new_post = Post(title=request.form['title'], 
                    content=request.form['content'],
                    user_id=user.id)
    
    db.session.add(new_post)
    db.session.commit()

    return redirect(f'/users/{user.id}')


@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """display post info"""

    post = Post.query.get(post_id)
    return render_template('post.html', post=post)


@app.route('/posts/<int:post_id>/edit')
def show_edit_post(post_id):
    """display edit post page"""

    post = Post.query.get(post_id)
    return render_template('edit-post.html', post=post)


@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def handle_edit_post(post_id):
    """edit post data in db"""

    post = Post.query.get(post_id)

    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()

    return redirect(f'/users/{post.user_id}')

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def handle_delete_post(post_id):

    post = Post.query.get(post_id)
    db.session.delete(post)
    db.session.commit()

    return redirect(f'/users/{post.user_id}')
