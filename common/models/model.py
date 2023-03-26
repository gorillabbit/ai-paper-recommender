from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# ユーザーテーブル
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    interests = db.Column(db.String(255))

    def __init__(self, username, password, email, interests):
        self.username = username
        self.password = password
        self.email = email
        self.interests = interests

# 論文テーブル
class Paper(db.Model):
    __tablename__ = 'papers'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    authors = db.Column(db.String(255))
    abstract = db.Column(db.Text())
    link = db.Column(db.String(255), nullable=False)
    interests = db.Column(db.String(255))

    def __init__(self, title, authors, abstract, link, interests):
        self.title = title
        self.authors = authors
        self.abstract = abstract
        self.link = link
        self.interests = interests

# 要約テーブル
class Summary(db.Model):
    __tablename__ = 'summaries'
    id = db.Column(db.Integer, primary_key=True)
    paper_id = db.Column(db.Integer, db.ForeignKey('papers.id'), nullable=False)
    summary = db.Column(db.Text(), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, paper_id, summary):
        self.paper_id = paper_id
        self.summary = summary

# レコメンド履歴テーブル
class History(db.Model):
    __tablename__ = 'histories'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    paper_id = db.Column(db.Integer, db.ForeignKey('papers.id'), nullable=False)
    viewed_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, user_id, paper_id):
        self.user_id = user_id
        self.paper_id = paper_id

if __name__ == '__main__':
    # Flaskアプリケーションのインスタンス化
    app = Flask(__name__)

    # app.configの設定

    # dbの初期化
    db.init_app(app)

    # データベースの作成
    with app.app_context():
        db.create_all()