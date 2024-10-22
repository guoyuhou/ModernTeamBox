from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User, Room, Booking
from flask_wtf.csrf import CSRFProtect
from urllib.parse import urlparse

csrf = CSRFProtect(app)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html',    title='首页')

@app.route('/rooms')
def rooms():
    rooms = Room.query.all()
    return render_template('rooms.html', title='房间列表', rooms=rooms)

@app.route('/booking', methods=['GET', 'POST'])
@login_required
def booking():
    if request.method == 'POST':
        # 处理预订逻辑
        new_booking = Booking(
            user_name=request.form['name'],
            user_email=request.form['email'],
            check_in=request.form['check_in'],
            check_out=request.form['check_out'],
            room_id=request.form['room_id']
        )
        db.session.add(new_booking)
        db.session.commit()
        return redirect(url_for('booking_confirmation'))
    
    rooms = Room.query.all()
    return render_template('booking.html', title='预订', rooms=rooms)

@app.route('/booking_confirmation')
def booking_confirmation():
    return render_template('booking_confirmation.html', title='预订确认')

@app.route('/about')
def about():
    return render_template('about.html', title='关于我们')

@app.route('/contact')
def contact():
    return render_template('contact.html', title='联系我们')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('无效的用户名或密码')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlparse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='登录', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('恭喜，您已成功注册！')
        return redirect(url_for('login'))
    return render_template('register.html', title='注册', form=form)
