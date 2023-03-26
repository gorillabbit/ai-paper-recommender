from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, Email
from werkzeug.security import generate_password_hash
from model import db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'secret_key'
db.init_app(app)


class RegisterForm(FlaskForm):
    username = StringField('ユーザー名', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('パスワード', validators=[InputRequired(), Length(min=8, max=50)])
    email = StringField('メールアドレス', validators=[InputRequired(), Email(message='メールアドレスの形式が不正です。')])
    submit = SubmitField('登録')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST':
        username = form.username.data
        password = form.password.data
        email = form.email.data
        hashed_password = generate_password_hash(password)
        user = User(username=username, password=hashed_password, email=email)
        db.session.add(user)
        db.session.commit()
        return 'ユーザー登録が完了しました。'

    return render_template('register.html', form=form)


if __name__ == '__main__':
    app.run()
