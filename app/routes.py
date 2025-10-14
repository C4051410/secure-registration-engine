from flask import Blueprint, render_template, request, redirect, url_for, current_app, flash
from .forms import RegistrationForm
import bleach
from datetime import datetime


main = Blueprint('main', __name__)


# Whitelist of tags and attributes for bleach
ALLOWED_TAGS = [
'b', 'i', 'u', 'em', 'strong', 'a', 'p', 'ul', 'ol', 'li'
]
ALLOWED_ATTRIBUTES = {
'a': ['href', 'title', 'rel']
}
ALLOWED_PROTOCOLS = ['http', 'https', 'mailto']




def client_ip():
# In production behind proxy, use X-Forwarded-For with appropriate trust proxy settings
if request.headers.get('X-Forwarded-For'):
return request.headers.get('X-Forwarded-For').split(',')[0].strip()
return request.remote_addr or 'unknown'




@main.route('/', methods=['GET'])
def home():
return redirect(url_for('main.register'))




@main.route('/register', methods=['GET', 'POST'])
def register():
form = RegistrationForm()
ip = client_ip()
timestamp = datetime.utcnow().isoformat() + 'Z'


if form.validate_on_submit():
# Sanitize bio using bleach with the whitelisted tags/attributes
raw_bio = form.bio.data or ''
cleaned_bio = bleach.clean(
raw_bio,
tags=ALLOWED_TAGS,
attributes=ALLOWED_ATTRIBUTES,
protocols=ALLOWED_PROTOCOLS,
strip=True
)


# If cleaning removed content or tags, log a warning
if cleaned_bio != (raw_bio or ''):
current_app.logger.warning(
f"{timestamp} - WARNING - Bio sanitized for user={form.username.data} ip={ip}"
)


# Here we would create the user in a database. For the task, simulate creation
current_app.logger.info(
f"{timestamp} - INFO - Registration successful for user={form.username.data} ip={ip}"
)


flash('Registration successful!', 'success')


# Display the sanitized bio safely (it is already cleaned)
return render_template('register.html', form=form, success=True, bio=cleaned_bio)


else:
# If POST and form did not validate, log details
if request.method == 'POST':
# Collect error details
errors = []
for field, errlist in form.errors.items():
for e in errlist:
errors.append(f"{field}: {e}")


current_app.logger.warning(
f"{timestamp} - WARNING - Registration failed for user={form.username.data} ip={ip} errors={' | '.join(errors)}"
)


# If username is reserved we already raise a ValidationError, but add an explicit log
if (form.username.data or '').lower() in {'admin', 'root', 'superuser'}:
current_app.logger.warning(f"{timestamp} - WARNING - Attempt to use reserved username by ip={ip}")


# GET or failed POST
return render_template('register.html', form=form, success=False, bio='')