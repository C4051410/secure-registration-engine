from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp, ValidationError
import re


# Reserved usernames and common passwords
RESERVED_USERNAMES = {'admin', 'root', 'superuser'}
COMMON_PASSWORDS = {
'password123', 'admin', '123456', 'qwerty', 'letmein',
'welcome', 'iloveyou', 'abc123', 'monkey', 'football'
}


ALLOWED_EMAIL_TLDS = ('.edu', '.ac.uk', '.org')




def username_not_reserved(form, field):
uname = (field.data or '').lower()
if uname in RESERVED_USERNAMES:
raise ValidationError('This username is reserved. Choose another.')




def email_tld_check(form, field):
email = (field.data or '').lower()
if not any(email.endswith(tld) for tld in ALLOWED_EMAIL_TLDS):
raise ValidationError('Email domain not allowed. Use .edu, .ac.uk or .org addresses.')




def password_policy_check(form, field):
pwd = field.data or ''
uname = (form.username.data or '')
email = (form.email.data or '')


if len(pwd) < 12:
raise ValidationError('Password must be at least 12 characters long.')
if re.search(r"\s", pwd):
raise ValidationError('Password must not contain whitespace characters.')
if not re.search(r'[A-Z]', pwd):
raise ValidationError('Password must contain at least one uppercase letter.')
if not re.search(r'[a-z]', pwd):
raise ValidationError('Password must contain at least one lowercase letter.')
if not re.search(r'[0-9]', pwd):
raise ValidationError('Password must contain at least one digit.')
if not re.search(r'[!@#$%^&*()_+\-=[\]{};:\"\\|,.<>/?`~]', pwd):
raise ValidationError('Password must contain at least one special character.')


low = pwd.lower()
if uname and uname.lower() in low:
raise ValidationError('Password must not contain the username.')
if email:
localpart = email.split('@')[0]
if localpart and localpart.lower() in low:
raise ValidationError('Password must not contain the email local-part.')


if pwd.lower() in COMMON_PASSWORDS:
raise ValidationError('Password is too common. Choose a stronger password.')




class RegistrationForm(FlaskForm):
username = StringField(
'Username',
validators=[
DataRequired(),
Length(min=3, max=30),
Regexp(r'^[A-Za-z_]+$', message='Username may only contain letters and underscores.'),
username_not_reserved
]
)


email = StringField(
'Email',
validators=[
DataRequired(),
Email(message='Invalid email address.'),
email_tld_check
]
)


password = PasswordField('Password', validators=[DataRequired(), password_policy_check])
confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match.')])


bio = TextAreaField('Bio / Comment (optional)')


submit = SubmitField('Register')