from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class SignupForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired("Username required!")])
    first_name = StringField("First Name", validators=[DataRequired("First name required!")])
    last_name = StringField("Last Name", validators=[DataRequired("Last name required!")])
    email = StringField("E-Mail", validators=[DataRequired("E-mail required!"), Email("Please enter a valid e-mail!")])
    password = PasswordField("Password", validators=[DataRequired("Password required!"), Length(min=5, message=("Password must be at least 5 characters."))])
    submit = SubmitField("Sign up!")

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired("Username required!")])
    password = PasswordField('Password', validators=[DataRequired("Password required!")])
    submit = SubmitField("Log in!")