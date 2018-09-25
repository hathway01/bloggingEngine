from flask import render_template, session, redirect, url_for, request
from app import app
from .forms import RegisterForm,LoginForm,BlogForm,SearchForm
from .models import db, User,Post

@app.errorhandler(404)
def not_found_error(error):
    return render_template('not_found.html')


@app.errorhandler(500)
def internal_error(error):
    return render_template('internal_error.html')

@app.route('/')
@app.route('/index')
def index():
    form = SearchForm()
    if 'name' not in session:
        session['name'] =None
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('index.html',title='Home',name=session['name'],posts=posts,searchform=form)

@app.route('/search',methods=['POST'])
def search():
    if request.method == 'POST':
        text = request.form['text']
    search_posts = Post.query.filter_by(title = text ).all()
    form = SearchForm()
    return render_template('index.html', title='Home', name=session['name'], searchform=form, posts=search_posts)

@app.route('/mypost')
def mypost():
    searchform = SearchForm()
    myposts = Post.query.filter_by(author=session['name']).order_by(Post.timestamp.desc()).all()
    return render_template('mypost.html',title='My Posts',name=session['name'],myposts=myposts,searchform=searchform)


@app.route('/post',methods=['GET','POST'])
def post():
    form = BlogForm()
    searchform = SearchForm()
    if request.method == 'POST':
        if form.validate() == False:
            return render_template('post.html',title='Post',name=session['name'], form=form, searchform=searchform)
        else:
            post = Post(form.title.data,form.content.data,session['name'])
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('index'))
    elif request.method == 'GET':
        return render_template('post.html',title='Post',name=session['name'], form=form,searchform=searchform)


@app.route('/about')
def about():
    form = SearchForm()
    return render_template('about.html',title='About',name=session['name'],searchform=form)



@app.route('/register', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    searchform = SearchForm()
    if request.method == 'POST':
        if form.validate() == False:
            return render_template('register.html', form=form, searchform=searchform)
        else:
            user = User(form.username.data,form.email.data,form.password.data)
            db.session.add(user)
            db.session.commit()
            session['name'] = user.username
            return redirect(url_for('index'))
    elif request.method == 'GET':
        return render_template('register.html', form=form, searchform=searchform)

@app.route('/logout')
def logout():
    session['name'] = None
    return redirect(url_for('index'))


@app.route('/login',methods=['GET','POST'])
def login():
    searchform = SearchForm()
    form = LoginForm()
    if request.method == 'POST':
        if form.validate() == False:
            return render_template('login.html', form=form, searchform=searchform)
        else:
            user = User.query.filter_by(email=form.email.data.lower()).first()
            session['name'] = user.username
            return redirect(url_for('index'))
    elif request.method == 'GET':
        return render_template('login.html', form=form, searchform=searchform)


@app.route('/update/<id>')
def update(id):
    post = Post.query.filter_by(id=id,author=session['name']).first()
    if post:
        form = BlogForm()
        form.title.data = post.title
        form.content.data = post.body
        Post.query.filter_by(id=id, author=session['name']).delete()
        db.session.commit()
        return render_template('post.html', title='Post', name=session['name'], form=form)
    else:
        return redirect(url_for('mypost'))


@app.route('/delete/<id>')
def delete(id):
    Post.query.filter_by(id=id,author=session['name']).delete()
    db.session.commit()
    return redirect(url_for('mypost'))