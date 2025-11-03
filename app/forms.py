from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp, ValidationError
import re

# --- Part A & B: Reserved Words and Policy Data ---
RESERVED_USERNAMES = {'admin', 'root', 'superuser'}
COMMON_PASSWORDS = {
    'password123', 'admin', '123456', 'qwerty', 'letmein',
    'welcome', 'iloveyou', 'abc123', 'monkey', 'football'
}
ALLOWED_EMAIL_TLDS = ('.edu', '.ac.uk', '.org')


# --- Part A: Custom Semantic Validators ---
def username_not_reserved(form, field):
    uname = (field.data or '').lower()
    if uname in RESERVED_USERNAMES:
        raise ValidationError('This username is reserved. Choose another.')


def email_tld_check(form, field):
    email = (field.data or '').lower()
    if not any(email.endswith(tld) for tld in ALLOWED_EMAIL_TLDS):
        raise ValidationError('Email domain not allowed. Use .edu, .ac.uk or .org addresses.')


# --- Part B: Custom Password Policy Validator ---
def password_policy_check(form, field):
    pwd = field.data or ''
    uname = (form.username.data or '')
    email = (form.email.data or '')

    # 1. Minimum length
    if len(pwd) < 12:
        raise ValidationError('Password must be at least 12 characters long.')

    # 2. No whitespace
    if re.search(r"\s", pwd):
        raise ValidationError('Password must not contain whitespace characters.')

    # 3. Complexity checks (uppercase, lowercase, digit, special character)
    if not re.search(r'[A-Z]', pwd):
        raise ValidationError('Password must contain at least one uppercase letter.')
    if not re.search(r'[a-z]', pwd):
        raise ValidationError('Password must contain at least one lowercase letter.')
    if not re.search(r'[0-9]', pwd):
        raise ValidationError('Password must contain at least one digit.')
    # Special characters: using a broad range
    if not re.search(r'[!@#$%^&*()_+\-=[\]{};:\"\\|,.<>/?`~]', pwd):
        raise ValidationError('Password must contain at least one special character.')

    # 4. Must not contain username or email local-part
    low_pwd = pwd.lower()
    if uname and uname.lower() in low_pwd:
        raise ValidationError('Password must not contain the username.')
    if email:
        localpart = email.split('@')[0]
        if localpart and localpart.lower() in low_pwd:
            raise ValidationError('Password must not contain the email local-part.')

    # 5. Must not be a common password
    if low_pwd in COMMON_PASSWORDS:
        raise ValidationError('Password is too common. Choose a stronger password.')


# --- Registration Form Definition (Part A) ---
class RegistrationForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            Length(min=3, max=30),
            Regexp(r'^[A-Za-z_]+$', message='Username may only contain letters and underscores.'),
            username_not_reserved  # Semantic Validation
        ]
    )

    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(message='Invalid email address.'),
            email_tld_check  # Semantic Validation
        ]
    )

    password = PasswordField('Password', validators=[DataRequired(), password_policy_check])

    # Confirms Part A requirement: Must match the original password
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[DataRequired(), EqualTo('password', message='Passwords must match.')]
    )

    bio = TextAreaField('Bio / Comment (optional)')

    submit = SubmitField('Register')