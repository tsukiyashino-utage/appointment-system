# app.py

# Auther: hhh5460
# Time: 2018/10/05
# Address: DongGuan YueHua

from functools import wraps
from flask import Flask, request, render_template, redirect, url_for, flash, session, jsonify

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, or_

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.secret_key = '\xc9ixnRb\xe40\xd4\xa5\x7f\x03\xd0y6\x01\x1f\x96\xeao+\x8a\x9f\xe4'

db = SQLAlchemy(app)

############################################
# 数据库
############################################

# 定义ORM
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)
    year = db.Column(db.String(80))
    month = db.Column(db.String(80))
    day = db.Column(db.String(80))

    def __repr__(self):
        return '<User %r>' % self.username


# 创建表格、插入数据
@app.before_first_request
# 用户数据
def create_db():
    db.create_all()

    guestes = [User(username='20206521', password='20206521', email='627235787@qq.com', year='0', month='0', day='0'),
               User(username='20206074', password='20206074', email='guest2@example.com', year='0', month='0', day='0')]
    db.session.add_all(guestes)
    db.session.commit()


############################################
# 辅助函数、装饰器
############################################

# 登录检验（用户名、密码验证）
def valid_login(username, password):
    user = User.query.filter(and_(User.username == username, User.password == password)).first()
    if user:
        return True
    else:
        return False

def valid_alogin(username, password):
    if username=='admin' and password=='root':
        return True
    else:
        return False


# 注册检验（用户名、邮箱验证）
def valid_regist(username, email):
    user = User.query.filter(or_(User.username == username, User.email == email)).first()
    if user:
        return False
    else:
        return True


# 登录
def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # if g.user:
        if session.get('username'):
            return func(*args, **kwargs)
        else:
            return redirect(url_for('login', next=request.url))  #

    return wrapper


############################################
# 路由
############################################


# 1.主页
@app.route('/')
def home():
    return render_template('home.html', username=session.get('username'))


# 2.1 用户登录
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'], request.form['password']):
            flash("成功登录！")
            session['username'] = request.form.get('username')
            return redirect(url_for('panel'))
        else:
            error = '错误的用户名或密码！'

    return render_template('login.html', error=error)

# 2.2 管理员登陆
@app.route('/administrator', methods=['GET', 'POST'])
def administrator():
    error = None
    if request.method == 'POST':
        if valid_alogin(request.form['username'], request.form['password']):
            flash("成功登录！")
            session['username'] = request.form.get('username')
            return redirect(url_for('adminpanel'))
        else:
            error = '错误的用户名或密码！'

    return render_template('administrator.html', error=error)


# 3.注销
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))


# 4.注册
@app.route('/regist', methods=['GET', 'POST'])
def regist():
    error = None
    if request.method == 'POST':
        if request.form['password1'] != request.form['password2']:
            error = '两次密码不相同！'
        elif valid_regist(request.form['username'], request.form['email']):
            user = User(username=request.form['username'], password=request.form['password1'],
                        email=request.form['email'], year='0', month='0', day='0')
            db.session.add(user)
            db.session.commit()

            flash("成功注册！")
            return redirect(url_for('login'))
        else:
            error = '该用户名或邮箱已被注册！'

    return render_template('regist.html', error=error)


# 5.1 用户个人中心
@app.route('/panel')
@login_required
def panel():
    username = session.get('username')
    user = User.query.filter(User.username == username).first()
    return render_template("panel.html", user=user)

# 用户提交预约
@app.route('/get_panel', methods=['GET', 'POST'])
def get_panel():
    if request.method == 'POST':

        year = request.form.get('year')
        month = request.form.get('month')
        day = request.form.get('day')
        user ={"year": year,  "month": month,  "day": day}

        username = session.get('username')
        flag = User.query.filter(User.username == username).first()
        if flag:
            flag.year = year
            flag.month = month
            flag.day = day
            db.session.commit()
            return jsonify(user)


# 5.2 管理员中心
@app.route('/adminpanel')
@login_required
def adminpanel():
    username = session.get('username')
    user = User.query.filter(User.username == username).first()
    return render_template("adminpanel.html", user=user)

# 管理员界面
@app.route('/get_adminpanel', methods=['GET', 'POST'])
def get_adminpanel():
    if request.method == 'GET':
        num_user = User.query.count()
        users = User.query.all()
        user = []
        for i in range(num_user):
            temp = {"username": users[i].username, "email": users[i].email, "year":users[i].year, "month":users[i].month, "day":users[i].day}
            user.append(temp)
        return jsonify(user)




if __name__ == '__main__':
    app.run(debug=True)
