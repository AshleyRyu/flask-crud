from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import datetime

app = Flask(__name__)
app.secret_key = 'asdf'



app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db_flask.sqlite3'
db = SQLAlchemy(app)

migrate = Migrate(app, db)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.String(80), nullable=False)
    
    def __init__(self, username, email):
        self.username = username
        self.email = email
        self.created_at = datetime.datetime.now().strftime("%D")
    
    def __repr__(self):
        return f'{self.id} : {self.username}'
        # return '<User %r>' % self.username

@app.route('/')
def index():
    users = User.query.all()
    # type(users) : list 타입
    # list element : user 인스턴스
    return render_template('index.html', users = users)
    
@app.route('/users/new')
def new_user():
    return render_template('new.html')
    # return redirect('/')
    
# @app.route('/users/create')
# def create_user():
#     username = request.args.get('username') # Ashley
#     email = request.args.get('email') # Ash@ash
#     # user  = User (username = Ashley, email = Ash@ash)
#     user = User(username = username, email = email)
#     db.session.add(user)
#     db.session.commit()
#     return render_template('create.html', username = user.username, email = user.email)
@app.route('/users/create', methods=["POST"]) #주소창으로 넘어가냐, 안보이게 넘어가냐 차이
def create_user():
    username = request.form.get('username') # Ashley
    email = request.form.get('email') # Ash@ash
    # user  = User (username = Ashley, email = Ash@ash)
    user = User(username = username, email = email)
    db.session.add(user)
    db.session.commit()
    # return render_template('create.html', username = user.username, email = user.email)
    return redirect('/')

@app.route('/users/read/<int:id>')
def read_user(id):
    user = User.query.get(id)
    return render_template('read.html', user = user)
    
# @app.route('/users/delete/<int:id>')
# def delete_user(id):
#     user = User.query.get(id)
#     db.session.delete(user)
#     db.session.commit()
#     # return render_template('index.html', user = user)
#     return redirect('/')
@app.route('/users/delete/<int:id>')
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    flash(f'{user.username}가 삭제되었습니다.', 'danger')
    # return render_template('index.html', user = user)
    return redirect('/')
    
@app.route('/users/edit/<int:id>')
def edit_user(id):
    user = User.query.get(id)
    return render_template('edit.html', user=user)
    
@app.route('/users/update/<int:id>', methods=["POST"])
def update_user(id):
    user = User.query.get(id)
    user.username = request.form.get('username')
    user.email = request.form.get('email')
    db.session.commit()
    flash('수정되었습니다.', 'success')
    return redirect('/')
    
if __name__ == '__main__':
    app.run(host = '0.0.0.0', port='8080', debug=True)
    