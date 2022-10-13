from flask import Flask, request, json
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_bcrypt import Bcrypt
from flask_cors import CORS
import sys
import logging


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:captainamerica55443@localhost/post_memories'
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
CORS(app)

app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"User: {self.username}"

    def __init__(self, username, password):
        self.username = username
        self.password = password


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    quote = db.Column(db.String(400), nullable=False)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    comment = db.Column(db.String(400), nullable=False)
    postId = db.Column(db.String(400), nullable=False)


def format_register(prop):
    return {
        "id": prop.id,
        "username": prop.username,
        "password": prop.password
    }


def format_login(log):
    return {
        "id": log.id,
        "username": log.username,
        "password": log.password
    }


def format_post(post):
    return {
        "id": post.id,
        "userId": post.userId,
        "username": post.username,
        "quote": post.quote
    }


def format_comment(comment):
    return {
        "id": comment.id,
        "userId": comment.userId,
        "username": comment.username,
        "comment": comment.comment,
        "postId": comment.postId
    }


@app.route('/')
def home():
    return "Hello Server is Working!"


@app.route('/register', methods=['POST'])
def register():

    log_username = request.json['username']
    log_password = request.json['password']
    new_user = User(username=log_username, password=log_password)
    db.session.add(new_user)
    db.session.commit()
    return format_register(new_user)


@app.route('/createPost', methods=["POST"])
def create_post():

    post_userId = request.json['userId']
    post_username = request.json['username']
    post_quote = request.json['quote']

    new_post = Post(userId=post_userId,
                    username=post_username, quote=post_quote)
    db.session.add(new_post)
    db.session.commit()
    return format_post(new_post)


@app.route('/comment', methods=["POST"])
def comment():
    com_userId = request.json['userId'],
    com_username = request.json['username'],
    com_comment = request.json['comment'],
    com_postId = request.json['postId']
    new_comment = Comment(userId=com_userId, username=com_username,
                          comment=com_comment, postId=com_postId)
    db.session.add(new_comment)
    db.session.commit()
    return format_comment(new_comment)


@app.route('/getComment', methods=['GET'])
def get_comment():
    comments = Comment.query.order_by(Comment.id.asc()).all()
    comment_list = []
    for comment in comments:
        comment_list.append(format_comment(comment))
    return {'comments': comment_list}


@app.route('/getPosts', methods=["GET"])
def get_posts():
    posts = Post.query.order_by(Post.id.asc()).all()
    post_list = []
    for post in posts:
        post_list.append(format_post(post))
    return {'posts': post_list}


@app.route('/login', methods=['POST'])
def login():
    loggedUser = request.json['username']

    log_user = User.query.filter_by(username=loggedUser).one()
    print(log_user)
    return format_login(log_user)


if (__name__) == "__main__":
    app.run(debug=True)
