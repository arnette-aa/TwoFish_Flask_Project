from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, DataRequired, ValidationError
from models import User

class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Pleate try a different username')

    username = StringField(label='Username:', validators=[Length(min=5, max = 32), DataRequired()])
    password = PasswordField(label='Password:', validators=[Length(min=5, max = 32), DataRequired()])
    password_Confirm = PasswordField(label='Confirm password', validators=[EqualTo('password'), DataRequired()])
    submit = SubmitField(label='Create Account')

class LoginForm(FlaskForm):
    username = StringField(label='Username:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')

class TaskForm(FlaskForm):
    content = StringField(validators=[DataRequired()])
    submit = SubmitField(label='Add Task')


