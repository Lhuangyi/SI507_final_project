#! /usr/bin/env python3
from flask import Flask
import json
from flask import render_template, request, redirect, flash, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash  # 密码保护，使用hash方法
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired
from flask_wtf import Form
from wtforms.fields import simple
from wtforms import validators
from wtforms import widgets

app = Flask(__name__)

app.debug = True
app.use_reloader = True
app.secret_key = 'tbPython'
app.config['SECRET_KEY'] = 'hard to guess string for app security adgsdfsadfdflsdfsj'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./courses.db'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
session = db.session
bootstrap = Bootstrap(app)


def upload_data():
    with open('courses.json') as f:
        response_json = f.read()
        data = json.loads(response_json)

        for i in data:
            dict = data[i]
            uni = University(name=i)
            db.session.add(uni)
            db.session.commit()
            instructors = dict['instructors']
            for ins in instructors:
                instructor = Instructor(name=ins, university_id=uni.id)
                db.session.add(instructor)
                db.session.commit()
            courses = dict['courses']
            for c in courses:
                course = Course(title=c, instructor_id=instructor.id, university_id=uni.id)
                db.session.add(course)
                db.session.commit()


c_u = db.Table('c_u',
                    db.Column('course_id', db.Integer, db.ForeignKey('course.id'),primary_key=True),
                    db.Column('uesr_id', db.Integer, db.ForeignKey('user.id'),primary_key=True))


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(200), nullable=False)  # 内部使用
    courses = db.relationship('Course', secondary='c_u', backref='user')

    @property
    def password(self):  # 定义一个外部使用的密码
        return self.password

    @password.setter  # 设置密码加密
    def password(self, row_password):
        self.password = generate_password_hash(row_password)

    def check_password(self, row_password):  # 定义一个反向解密的函数
        result = check_password_hash(self.password, row_password)
        return result


class University(db.Model):
    __tablename__ = "university"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    courses = db.relationship('Course', backref='university')
    instructors = db.relationship('Instructor', backref='university')


class Course(db.Model):
    __tablename__ = "course"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    description = db.Column(db.String(500))
    university_id = db.Column(db.Integer, db.ForeignKey('university.id'))
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructor.id'))

    def __repr__(self):
        return '<Course %r>' % self.title


class Instructor(db.Model):
    __tablename__ = "instructor"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    position = db.Column(db.String(500))
    university_id = db.Column(db.Integer, db.ForeignKey('university.id'))
    courses = db.relationship('Course', backref='instructor')

    def __repr__(self):
        return '<Instructor %r>' % self.name


#############route funcions#####################
@app.route('/',methods=["GET","POST"])
def homepage():
    universities = University.query.all()
    return render_template('index.html', universities=universities)


@app.route('/university')
def university():
    university_id=request.args.get('id')
    university = University.query.filter(University.id == university_id).first()
    return render_template('detail.html', university=university)


@app.route('/add', methods=["GET", "POST"])
def add():
    if request.method == "POST":
        uni_form = AddUniForm()
        universities = University.query.all()
        # 1.调用wtf的函数实现验证
        if uni_form.validate_on_submit():
            # 2.验证通过后获取数据
            university_name = uni_form.name.data
            instructor_name = uni_form.instructors.data
            course_name = uni_form.courses.data
            # 3.判断作者是否存在
            university = University.query.filter_by(name=university_name).first()
            if university:
                flash('University has exited')
                instructor = Instructor.query.filter_by(name=instructor_name).first()
                # 4.如果作者存在
                if instructor:
                    flash('Instructor has exited')
                    course = Course.query.filter_by(title=course_name).first()
                    if course:
                        flash('Course has exited')
                    else:
                        try:
                            new_course = Course(title=course_name, instructor_id=instructor.id, university_id=university.id)
                            db.session.add(new_course)
                            db.session.commit()
                        except Exception as e:
                            print(e)
                            flash('Fail to add course')
                            # 数据库回滚
                            db.session.rollback()
                # 5.如果作者不存在
                else:
                    try:
                        new_instructor = Instructor(name=instructor_name, university_id=university.id)
                        db.session.add(new_instructor)
                        db.session.commit()

                        new_course = Course(title=course_name, instructor_id=new_instructor.id, university_id=university.id)
                        db.session.add(new_course)
                        db.session.commit()
                    except Exception as e:
                        print(e)
                        flash('Fail to add instructor and course')
                        db.session.rollback()
            else:
                try:
                    new_university = University(name=university_name)
                    db.session.add(new_university)
                    db.session.commit()

                    new_instructor = Instructor(name=instructor_name, university_id=new_university.id)
                    db.session.add(new_instructor)
                    db.session.commit()

                    new_course = Course(title=course_name, instructor_id=new_instructor.id, university_id=new_university.id)
                    db.session.add(new_course)
                    db.session.commit()

                except Exception as e:
                    print(e)
                    flash('Fail to add university, instructor,course')
                    db.session.rollback()
        else:
            # 6.验证不通过则提示错误
            if request.method == 'POST':
                flash('参数错误')
        return redirect('/')
    else:
        uni_form = AddUniForm()
        universities = University.query.all()
        courses = Course.query.all()
        return render_template('adduni.html', courses=courses, form=uni_form, universities=universities)


@app.route('/delete_university/<university_id>')
def delete_university(university_id):
    university = University.query.get(university_id)
    if university:
        try:
            Course.query.filter_by(university_id=university.id).delete()
            db.session.delete(university)
            db.session.commit()

        except Exception as e:
            print(e)
            flash('Failed')
            db.session.rollback()
    else:
        flash('Cannot find the university')

    return redirect('/')


@app.route('/delete_course/<course_id>')
def delete_course(course_id):
    course = Course.query.get(course_id)
    if course:
        try:
            db.session.delete(course)
            db.session.commit()
        except Exception as e:
            print(e)
            flash('Failed')
            db.session.rollback()
    else:
        flash("Can't find this course")
    return redirect('/')


@app.route('/delete_instructor/<instructor_id>')
def delete_instructor(instructor_id):
    instructor = Instructor.query.get(instructor_id)
    if instructor:
        try:
            Course.query.filter_by(instructor_id=instructor.id).delete()
            db.session.delete(instructor)
            db.session.commit()

        except Exception as e:
            print(e)
            flash('Failed')
            db.session.rollback()
    else:
        flash('Canot find the instructor')
    return redirect('/')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        form = LoginForm()
        return render_template('login.html',form=form)
    else:
        print(request.form)
        form = LoginForm(formdata=request.form)
        if form.validate():
            print('用户提交的数据通过格式验证，提交的值为：', form.data)
            user = User(username=form.name.data, password=form.pwd.data)
            if user:
                return render_template('success.html')
        else:
            print(form.errors)
        return render_template('login.html', form=form)


class LoginForm(Form):
    name = simple.StringField(
        label='username',
        validators=[
            validators.DataRequired(message='Username cannot be empty!'),
            validators.Length(min=2, max=18, message='Username must longer than%（min)d and shorter than%(max)d')
        ],
        widget=widgets.TextInput(),
        render_kw={'class': 'form-control'}
    )

    pwd = simple.PasswordField(
        label='password',
        validators=[
            validators.DataRequired(message='Password cannot be empty！'),
            validators.Length(min=6, message='Password must longer than%(min)d'),
            validators.Regexp(regex="^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%*?&])[A-Za-z\d$@$!%*?&]{8,}",
                              message="Password must be at least 6 characters, at least one uppercase letter,one lowercase letter, one digit and one special character"),
        ],
        widget=widgets.PasswordInput(),
        render_kw={'class': 'form-control'}

    )


class RegisterForm(Form):
    name = simple.StringField(
        label='username',
        validators=[
            validators.DataRequired()
        ],
        widget=widgets.TextInput(),
        render_kw={'class': 'form-control'},
        default='zxc'
    )

    pwd = simple.PasswordField(
        label='password',
        validators=[
            validators.DataRequired()
        ],
        widget=widgets.PasswordInput(),
        render_kw={'class': 'form-control'}
    )

    pwd_confirm = simple.PasswordField(
        label='confirm password',
        validators=[
            validators.DataRequired(message='Password cannot be empty！'),
            validators.EqualTo('pwd', 'Does not match!!')
        ],
        widget=widgets.PasswordInput(),
        render_kw={'class': 'form-control'}
    )

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

    def validate_pwd_confirm(self, field):
        '''
        自定义pwd_confirm规则,如： 与原密码是否一致
        :return:
        '''
        if field.data != self.data['pwd']:
            # raise validators.ValidationError('密码不一致')  #继续后续验证
            raise validators.StopValidation('Does not match!!')  # 不再后续验证


class AddUniForm(Form):
    name = StringField('name', validators=[DataRequired()])
    courses = StringField('courses', validators=[DataRequired()])
    instructors = StringField('instructor', validators=[DataRequired()])
    submit = SubmitField('submit')


if __name__ == '__main__':
    db.create_all()
    upload_data()
    app.run(debug=True)

