from flask import Flask
from flask import render_template, request, redirect, flash, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash  # 密码保护，使用hash方法
from wtforms import StringField,SubmitField
from wtforms.validators import  DataRequired
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

c_u = db.Table('c_u',
                    db.Column('course_id', db.Integer, db.ForeignKey('course.id'),primary_key=True),
                    db.Column('uesr_id', db.Integer, db.ForeignKey('user.id'),primary_key=True))


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
    comments = db.relationship('Comment', backref='comment')
    users = db.relationship('User', secondary = 'c_u', backref='course')
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


class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(20), nullable=False)
    content = db.Column(db.String(500),nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(200), nullable=False)  # 内部使用
    comments = db.relationship('Comment', backref='user')
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



#############route funcions######################
@app.route('/index',methods=["GET","POST"])
def homepage():
    universities = University.query.all()
    return render_template('index.html', universities=universities)


@app.route('/create',methods=["GET","POST"])
def add():
    course_form = AddCourseForm()
    universities = University.query.all()
    # 1.调用wtf的函数实现验证
    if course_form.validate_on_submit():
        # 2.验证通过后获取数据
        university_name = course_form.university.data
        instructor_name = course_form.instructor.data
        course_name = course_form.title.data
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
                        new_course = Course(title=course_name, instructor_id=instructor.id)
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
                    new_instructor = Instructor(name=instructor_name)
                    db.session.add(new_instructor)
                    db.session.commit()

                    new_course = Course(title=course_name, instructor_id=new_instructor.id)
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

                new_instructor = Instructor(name=instructor_name)
                db.session.add(new_instructor)
                db.session.commit()

                new_course = Course(title=course_name, instructor_id=new_instructor.id)
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
    courses = Course.query.all()
    return render_template('add.html', courses=courses, form=course_form, universities = universities)


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
    return redirect(url_for('index'))


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

    return render_template(url_for('index'))


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


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        form = RegisterForm(data={'gender': 1})
        return render_template('register.html', form=form)
    else:
        form = RegisterForm(formdata=request.form)
        if form.validate():
            print(request.form)
            print('用户提交数据格式验证成功，提交的值为：', form.data)
            user = User(username=form.name.data, password=form.pwd.data)
            obj1 = user
            session.add(obj1)
            session.commit()
            return render_template('show_course.html')
        else:
            print(form.errors)
            return render_template('register.html', form=form)

@app.route('/university/<university_id>', methods=["GET"])
def uni_detail(university_id):
    university = University.query.filter(University.id==university_id).first()
    return render_template('detail.html', university=university)


@app.route('/user/<user_id>', methods=['GET'])
def usercenter(user_id):
    user = User.query.filter(User.id==user_id).first()
    context = {
        'user': user
    }
    return render_template('user.html', **context)

# 读取前端页面数据，保存到数据库中


################################################

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
                              message="密码至少6个字符，至少一个大写字母，1个小写字母，1个数字和1个特殊字符"),
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


class AddCourseForm(Form):
    title = StringField('title', validators=[DataRequired()])
    instructor = StringField('instructor',validators=[DataRequired()])
    university = StringField('university', validators=[DataRequired()])
    submit = SubmitField('submit')


class AddUniForm(Form):
    name = StringField('name', validators=[DataRequired()])


if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    uni1 = University(name='Umich')
    uni2 = University(name='Stanford')
    uni3 = University(name='UCLA')
    db.session.add_all([uni1, uni2, uni3])
    db.session.commit()
    ins1 = Instructor(name='Jack', position='Professor', university_id=uni1.id)
    ins2 = Instructor(name='Tom', position='Professor', university_id=uni2.id)
    ins3 = Instructor(name='Ada', position='Professor', university_id=uni3.id)
    db.session.add_all([ins1,ins2,ins3])
    db.session.commit()
    c1 = Course(title='Java', description='good', instructor_id=ins1.id, university_id=uni1.id)
    c2 = Course(title='Python', description='fun',instructor_id=ins3.id, university_id=uni2.id)
    c3 = Course(title='Flask', description='fun',instructor_id=ins2.id, university_id=uni3.id)
    c4 = Course(title='ADS', description='good', instructor_id=ins1.id, university_id=uni1.id)
    c5 = Course(title='English', description='good', instructor_id=ins2.id, university_id=uni1.id)
    c6 = Course(title='Web', description='good', instructor_id=ins1.id, university_id=uni3.id)
    c7 = Course(title='Computer', description='good', instructor_id=ins1.id, university_id=uni1.id)

    db.session.add_all([c1, c2, c3,c4,c5,c6,c7])
    db.session.commit()

    app.run(debug=True)

