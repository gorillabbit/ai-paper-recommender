
from flask import Flask, render_template, request
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# MySQLの接続情報を設定
load_dotenv()
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_PORT'] = int(os.getenv('MYSQL_PORT'))  # ポート番号を整数に変換
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')
print(app.config)
#mysql = MySQL(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ルートページ
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/paper/<int:paper_id>')
def paper(paper_id):
    paper = Paper.query.get(paper_id)
    summary = paper.summary
    return render_template('paper.html', paper=paper, summary=summary)

# 論文一覧ページ
@app.route('/papers')
def papers():
    return render_template('papers.html')

# プレスリリース一覧ページ
@app.route('/press_releases')
def press_releases():
    return render_template('press_releases.html')

# ログインページ
@app.route('/login')
def login():
    return render_template('login.html')

# 新規登録ページ
@app.route('/signup')
def signup():
    return render_template('signup.html')

# APIエンドポイント
@app.route('/api/recommendations', methods=['POST'])
def api_recommendations():
    # リクエストデータからユーザーの興味や関心を取得
    user_interest = request.json['interest']

    # TODO: 要約レコメンドのロジックを実装

    # レスポンスとして要約記事を返す
    return jsonify({'summary': summary})

if __name__ == '__main__':
    app.run(debug=True)
