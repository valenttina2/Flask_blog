from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# import os
# import sys
# project_root = os.path.dirname(__file__)
# template_path = os.path.join(project_root, '../templates')
# static_path = os.path.join(project_root, '../static')
# app = Flask(__name__, template_folder=template_path, static_folder=static_path)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)

class Article(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    category = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<Article %r>' %self.id


@app.route('/')
def index():
    return  render_template("index.html")

@app.route('/about')
@app.route('/home')
def about():
    return render_template("about.html")

# @app.route('/user/<string:name>/<int:id>')
# def user(name, id):
#     return 'User page: '+name+'-'+str(id)

@app.route('/create_article', methods=['POST', 'GET'])
def create_article():
    if request.method == 'POST':
        title= request.form['title']
        intro =request.form['intro']
        text = request.form['text']
        category= request.form['category']
        article=Article(title=title, intro=intro, text=text, category=category)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')
        except:
            return "При добавлении статьи возникла ошибка"

    else:
        return render_template("create_article.html")

@app.route('/posts')
def posts():
    articles=Article.query.order_by(Article.date.desc()).all()
    return render_template("posts.html", articles=articles)

@app.route('/posts/<int:id>')
def post_detail(id):
    article=Article.query.get(id)
    return render_template("post_detail.html", article=article)

@app.route('/posts/<int:id>/update', methods=['POST', 'GET'])
def post_update(id):
    article = Article.query.get(id)

    if request.method == 'POST':
        article.title= request.form['title']
        article.intro =request.form['intro']
        article.text = request.form['text']
        article.category= request.form['category']

        try:
            db.session.commit()
            return redirect('/posts')
        except:
            return "При редактировании статьи возникла ошибка"
    else:
        article=Article.query.get(id)
        return render_template("post_update.html", article=article)


@app.route('/posts/<int:id>/delete')
def post_delete(id):
    article=Article.query.get_or_404(id)

    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/posts')
    except:
        return 'При удалении статьи возникла ошибка'



if __name__=='__main__':
    app.run(debug=True)