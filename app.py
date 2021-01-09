from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'

db = SQLAlchemy(app)

# Models
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(20), nullable=False, default='N/A')
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return 'Blog post ' + str(self.id)

# Now run the following in the terminal:
# from app import db
# db.create_all()
# from app import BlogPost
# db.session.add(BlogPost(title='Blog Post 1', content='lalalala', author='Hamza'))
# db.session.add(BlogPost(title='Blog Post 2', content='lalalala2', author='Aaron'))
# db.session.add(BlogPost(title='Blog Post 3', content='lalalala3', author='Jessica'))
# BlogPost.query.all()
# BlogPost.query.all()[0].date_posted

#### CRUD ###
# READ
# BlogPost.query.filter_by(author='Hamza').all()
# BlogPost.query.order_by(author='Hamza').all()
# BlogPost.query.get(2)

# DELETE
# db.session.delete(BlogPost.query.get(2))
# db.session.commit()

# UPDATE
# BlogPost.query.get(1).author = 'Erika'
# db.sessiom.commit()

# Base route
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/posts', methods=['GET', 'POST'])
def posts():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        new_post = BlogPost(title=post_title, content=post_content, author=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        all_posts = BlogPost.query.order_by(BlogPost.date_posted).all()
        return render_template('posts.html', posts=all_posts)

@app.route('/posts/delete/<int:id>')
def delete(id):
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')

@app.route('/posts/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        new_post = BlogPost(title=post_title, content=post_content, author=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        all_posts = BlogPost.query.order_by(BlogPost.date_posted).all()
        return render_template('create.html', posts=all_posts)


@app.route('/posts/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    post = BlogPost.query.get_or_404(id)

    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        post.author = request.form['author']
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('update.html', post=post)

# If we were to run the file locally this would run
if __name__ == "__main__":
    app.run(debug=True)



