from flask import Blueprint, render_template, request, redirect, url_for, current_app, flash
from .forms import RegistrationForm # Import the new form
import bleach # Used for Part C
from datetime import datetime

main = Blueprint('main', __name__)

# --- Part C: Whitelist for bleach ---
ALLOWED_TAGS = [
    'b', 'i', 'u', 'em', 'strong', 'a', 'p', 'ul', 'ol', 'li'
]
ALLOWED_ATTRIBUTES = {
    'a': ['href', 'title', 'rel']
}
ALLOWED_PROTOCOLS = ['http', 'https', 'mailto']

# --- Part D: Helper to get client IP ---
def client_ip():
    # Safely retrieve IP, considering proxies
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
    timestamp = datetime.utcnow().isoformat() + 'Z' # UTC Timestamp

    if form.validate_on_submit():
        # --- Part C: Sanitization ---
        raw_bio = form.bio.data or ''
        cleaned_bio = bleach.clean(
            raw_bio,
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRIBUTES,
            protocols=ALLOWED_PROTOCOLS,
            strip=True
        )

        # Log suspicious input (if content was stripped)
        if raw_bio and cleaned_bio != raw_bio:
            current_app.logger.warning(
                f"{timestamp} - WARNING - Bio sanitized (disallowed HTML tags stripped) for user={form.username.data} ip={ip}"
            )

        # Simulation of account creation
        current_app.logger.info(
            f"{timestamp} - INFO - Registration successful for user={form.username.data} ip={ip}"
        )

        flash('Registration successful! Check your logs.', 'success')

        # Part C: Display sanitized bio content safely (already cleaned by bleach)
        return render_template('register.html', form=form, success=True, bio=cleaned_bio)

    else:
        # --- Part D: Logging Validation Failures (WARNING) ---
        if request.method == 'POST':
            errors = []
            for field, errlist in form.errors.items():
                for e in errlist:
                    errors.append(f"{field}: {e}")

            # Log reserved username attempt explicitly
            if (form.username.data or '').lower() in {'admin', 'root', 'superuser'}:
                 current_app.logger.warning(f"{timestamp} - WARNING - Attempt to use reserved username by ip={ip}")

            # Log general validation failure
            current_app.logger.warning(
                f"{timestamp} - WARNING - Registration failed for user={form.username.data or 'N/A'} ip={ip} errors={' | '.join(errors)}"
            )

        # GET or failed POST
        return render_template('register.html', form=form, success=False, bio='')