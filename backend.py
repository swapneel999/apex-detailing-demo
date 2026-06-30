"""

RGDETAILING Secure Flask Backend

OWASP-compliant: rate limiting, IDOR prevention, input validation, password hashing.

"""

import os

import re

import uuid

import sqlite3

import secrets

import smtplib

import threading

from functools import wraps

from datetime import datetime

from email.mime.text import MIMEText

from email.mime.multipart import MIMEMultipart



import bcrypt

from flask import Flask, request, jsonify, session

from flask_cors import CORS

from flask_limiter import Limiter

from flask_limiter.util import get_remote_address



# ----------------------------------------------------------------

# App setup â€” all secrets from environment, never hardcoded

# ----------------------------------------------------------------

app = Flask(__name__)



_secret_key = os.environ.get('SECRET_KEY')

if not _secret_key:

    raise RuntimeError('SECRET_KEY environment variable is required')

app.secret_key = _secret_key



app.config.update(

    SESSION_COOKIE_HTTPONLY=True,

    SESSION_COOKIE_SAMESITE='Lax',

    SESSION_COOKIE_SECURE=os.environ.get('FLASK_ENV') == 'production',

    MAX_CONTENT_LENGTH=64 * 1024,  # 64KB request cap

)



# CORS restrict to configured origins only

_allowed_origins = os.environ.get('ALLOWED_ORIGINS', 'http://localhost:5000').split(',')

CORS(app, origins=[o.strip() for o in _allowed_origins], supports_credentials=True)



# Rate limiter â€” in-memory storage (swap to Redis in production)

limiter = Limiter(

    get_remote_address,

    app=app,

    default_limits=['200 per day', '50 per hour'],

    storage_uri='memory://',

)



# ----------------------------------------------------------------

# Database

# ----------------------------------------------------------------

DB_PATH = os.environ.get('DB_PATH', 'rgdetailing.db')





def get_db():

    conn = sqlite3.connect(DB_PATH)

    conn.row_factory = sqlite3.Row

    conn.execute('PRAGMA foreign_keys = ON')

    return conn





def init_db():

    with get_db() as conn:

        conn.execute('''

            CREATE TABLE IF NOT EXISTS quotes (

                id          TEXT    PRIMARY KEY,

                name        TEXT    NOT NULL,

                email       TEXT    NOT NULL,

                phone       TEXT    NOT NULL,

                vehicle     TEXT    NOT NULL,

                package     TEXT    NOT NULL,

                message     TEXT    NOT NULL DEFAULT '',

                created_at  TEXT    NOT NULL

            )

        ''')

        conn.execute('''

            CREATE TABLE IF NOT EXISTS admins (

                id            TEXT    PRIMARY KEY,

                username      TEXT    UNIQUE NOT NULL,

                password_hash TEXT    NOT NULL,

                created_at    TEXT    NOT NULL

            )

        ''')





# ----------------------------------------------------------------

# Input validation helpers

# ----------------------------------------------------------------

_EMAIL_RE = re.compile(r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$')

_PHONE_RE = re.compile(r'^(\+61|0)[2-9]\d{8}$')



ALLOWED_PACKAGES = frozenset({'CERAMIC_LITE', 'CERAMIC_PRO', 'APEX_CERAMIC'})





def validate_email(value):

    return bool(_EMAIL_RE.match(value))





def validate_phone(value):

    cleaned = re.sub(r'[\s\-()]', '', value)

    return bool(_PHONE_RE.match(cleaned))





def bad_request(message):

    return jsonify({'error': message}), 400





# ----------------------------------------------------------------

# Lead notification engine — fires in a background thread so the

# HTTP response is never blocked by SMTP latency

# ----------------------------------------------------------------

def _send_lead_notification(name, phone, email, vehicle, package, timestamp):

    smtp_server   = os.environ.get('SMTP_SERVER')

    smtp_port     = int(os.environ.get('SMTP_PORT', 587))

    sender        = os.environ.get('NOTIFICATION_EMAIL_SENDER')

    password      = os.environ.get('NOTIFICATION_EMAIL_PASSWORD')

    receiver      = os.environ.get('CLIENT_RECEIVER_EMAIL')



    if not all([smtp_server, sender, password, receiver]):

        return  # Silently skip if SMTP is not configured



    subject = '[CRITICAL LEAD] New Premium Detailing Inquiry - RGDETAILING'

    body = (

        '=========================================\n'

        'NEW LEAD CAPTURED FROM prototype FRONTEND\n'

        '=========================================\n'

        f'Name:              {name}\n'

        f'Phone:             {phone}\n'

        f'Email:             {email}\n'

        f'Vehicle Details:   {vehicle}\n'

        f'Requested Service: {package}\n'

        f'Timestamp:         {timestamp}\n'

        '=========================================\n'

        'Secure verification: Passed validation and CSRF checks.'

    )



    msg = MIMEMultipart()

    msg['From']    = sender

    msg['To']      = receiver

    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))



    try:

        with smtplib.SMTP(smtp_server, smtp_port) as server:

            server.starttls()

            server.login(sender, password)

            server.sendmail(sender, receiver, msg.as_string())

    except Exception:

        pass  # Never surface SMTP errors to the client





def _fire_notification(name, phone, email, vehicle, package, timestamp):

    """Launch notification in a daemon thread — non-blocking."""

    t = threading.Thread(

        target=_send_lead_notification,

        args=(name, phone, email, vehicle, package, timestamp),

        daemon=True,

    )

    t.start()



# ----------------------------------------------------------------

# Authorization decorator â€” IDOR/privilege-escalation prevention

# ----------------------------------------------------------------

def require_admin(f):

    @wraps(f)

    def decorated(*args, **kwargs):

        if not session.get('admin_id'):

            return jsonify({'error': 'Unauthorized'}), 401

        return f(*args, **kwargs)

    return decorated





# ----------------------------------------------------------------

# CSRF token endpoint

# ----------------------------------------------------------------

@app.route('/api/csrf-token', methods=['GET'])

@limiter.limit('60 per minute')

def get_csrf_token():

    if 'csrf_token' not in session:

        session['csrf_token'] = secrets.token_hex(32)

    return jsonify({'token': session['csrf_token']})





def verify_csrf(data):

    token    = data.get('csrf_token', '')

    expected = session.get('csrf_token', '')

    if not token or not expected:

        return False

    return secrets.compare_digest(token, expected)





# ----------------------------------------------------------------

# Public: Submit quote

# ----------------------------------------------------------------

@app.route('/api/quote', methods=['POST'])

@limiter.limit('5 per minute; 20 per hour')

def submit_quote():

    data = request.get_json(force=False, silent=True)

    if not isinstance(data, dict):

        return bad_request('Request body must be JSON.')



    if not verify_csrf(data):

        return jsonify({'error': 'Invalid or missing CSRF token.'}), 403



    # Explicit type validation on every field

    for field in ('name', 'email', 'phone', 'vehicle', 'package'):

        if field not in data:

            return bad_request(f'Missing required field: {field}')

        if not isinstance(data[field], str):

            return bad_request(f'Field "{field}" must be a string.')



    name    = data['name'].strip()

    email   = data['email'].strip().lower()

    phone   = data['phone'].strip()

    vehicle = data['vehicle'].strip()

    package = data['package'].strip().upper()

    message = data.get('message', '')



    if not isinstance(message, str):

        return bad_request('Field "message" must be a string.')

    message = message.strip()



    # Length bounds

    if not 2 <= len(name) <= 100:

        return bad_request('Name must be between 2 and 100 characters.')

    if not validate_email(email):

        return bad_request('Invalid email address.')

    if not validate_phone(phone):

        return bad_request('Invalid Australian phone number (e.g. 0412 345 678).')

    if not 2 <= len(vehicle) <= 100:

        return bad_request('Vehicle details must be between 2 and 100 characters.')

    if len(message) > 500:

        return bad_request('Message must not exceed 500 characters.')



    # Enum whitelist â€” prevents IDOR-class injection via package field

    if package not in ALLOWED_PACKAGES:

        return bad_request('Invalid package selection.')



    quote_id = str(uuid.uuid4())

    now      = datetime.utcnow().isoformat()



    try:

        with get_db() as conn:

            # Parameterized query â€” SQL injection is structurally impossible

            conn.execute(

                'INSERT INTO quotes (id, name, email, phone, vehicle, package, message, created_at)'

                ' VALUES (?, ?, ?, ?, ?, ?, ?, ?)',

                (quote_id, name, email, phone, vehicle, package, message, now)

            )

        _fire_notification(name, phone, email, vehicle, package, now)

        return jsonify({

            'success': True,

            'message': 'Quote request received. We will contact you within 24 hours.'

        }), 201

    except Exception:

        return jsonify({'error': 'Failed to save quote. Please try again.'}), 500





# ----------------------------------------------------------------

# Admin: Login

# ----------------------------------------------------------------

@app.route('/api/admin/login', methods=['POST'])

@limiter.limit('5 per minute')

def admin_login():

    data = request.get_json(force=False, silent=True)

    if not isinstance(data, dict):

        return bad_request('Request body must be JSON.')



    username = data.get('username', '')

    password = data.get('password', '')



    if not isinstance(username, str) or not isinstance(password, str):

        return bad_request('Username and password must be strings.')

    if not username.strip() or not password:

        return bad_request('Username and password are required.')



    username = username.strip()



    if len(username) > 64 or len(password) > 128:

        return bad_request('Input exceeds maximum allowed length.')



    try:

        with get_db() as conn:

            row = conn.execute(

                'SELECT id, password_hash FROM admins WHERE username = ?',

                (username,)

            ).fetchone()



        if row is None:

            # Constant-time dummy check prevents username enumeration via timing attack

            bcrypt.checkpw(b'dummy_password', b'$2b$12$aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')

            return jsonify({'error': 'Invalid credentials.'}), 401



        if bcrypt.checkpw(password.encode('utf-8'), row['password_hash'].encode('utf-8')):

            session.clear()

            session['admin_id'] = row['id']

            return jsonify({'success': True})



        return jsonify({'error': 'Invalid credentials.'}), 401



    except Exception:

        return jsonify({'error': 'Login failed. Please try again.'}), 500





# ----------------------------------------------------------------

# Admin: Logout

# ----------------------------------------------------------------

@app.route('/api/admin/logout', methods=['POST'])

@limiter.limit('60 per minute')

@require_admin

def admin_logout():

    session.clear()

    return jsonify({'success': True})





# ----------------------------------------------------------------

# Admin: List quotes â€” no user-supplied ID, no IDOR risk

# ----------------------------------------------------------------

@app.route('/api/admin/quotes', methods=['GET'])

@require_admin

@limiter.limit('30 per minute')

def list_quotes():

    try:

        with get_db() as conn:

            rows = conn.execute(

                'SELECT id, name, email, phone, vehicle, package, created_at'

                ' FROM quotes ORDER BY created_at DESC LIMIT 200'

            ).fetchall()

        return jsonify([dict(r) for r in rows])

    except Exception:

        return jsonify({'error': 'Failed to retrieve quotes.'}), 500





# ----------------------------------------------------------------

# Admin: Fetch single quote by opaque UUID â€” IDOR-safe

# ----------------------------------------------------------------

@app.route('/api/admin/quotes/<quote_id>', methods=['GET'])

@require_admin

@limiter.limit('60 per minute')

def get_quote(quote_id):

    # Validate UUID format before any DB interaction

    try:

        uuid.UUID(quote_id)

    except ValueError:

        return jsonify({'error': 'Invalid quote ID format.'}), 400



    try:

        with get_db() as conn:

            row = conn.execute(

                'SELECT * FROM quotes WHERE id = ?',

                (quote_id,)

            ).fetchone()



        if row is None:

            return jsonify({'error': 'Quote not found.'}), 404



        return jsonify(dict(row))

    except Exception:

        return jsonify({'error': 'Failed to retrieve quote.'}), 500





# ----------------------------------------------------------------

# Admin: One-time setup (disable via DISABLE_SETUP=true in env)

# ----------------------------------------------------------------

@app.route('/api/admin/setup', methods=['POST'])

@limiter.limit('3 per hour')

def admin_setup():

    if os.environ.get('DISABLE_SETUP', 'false').lower() == 'true':

        return jsonify({'error': 'Setup endpoint is disabled.'}), 403



    data = request.get_json(force=False, silent=True)

    if not isinstance(data, dict):

        return bad_request('Request body must be JSON.')



    username  = data.get('username', '').strip()

    password  = data.get('password', '')

    setup_key = data.get('setup_key', '')



    expected_key = os.environ.get('SETUP_KEY', '')

    if not expected_key or not secrets.compare_digest(setup_key, expected_key):

        return jsonify({'error': 'Invalid setup key.'}), 403



    if not isinstance(username, str) or not isinstance(password, str):

        return bad_request('Username and password must be strings.')

    if not 3 <= len(username) <= 64:

        return bad_request('Username must be between 3 and 64 characters.')

    if len(password) < 12:

        return bad_request('Password must be at least 12 characters.')



    # bcrypt with work factor 12 â€” adaptive slow hash, never MD5/SHA

    password_hash = bcrypt.hashpw(

        password.encode('utf-8'),

        bcrypt.gensalt(rounds=12)

    ).decode('utf-8')



    admin_id = str(uuid.uuid4())

    now      = datetime.utcnow().isoformat()



    try:

        with get_db() as conn:

            conn.execute(

                'INSERT INTO admins (id, username, password_hash, created_at) VALUES (?, ?, ?, ?)',

                (admin_id, username, password_hash, now)

            )

        return jsonify({'success': True, 'admin_id': admin_id}), 201

    except sqlite3.IntegrityError:

        return jsonify({'error': 'Username already exists.'}), 409

    except Exception:

        return jsonify({'error': 'Failed to create admin account.'}), 500





# ----------------------------------------------------------------

# Error handlers

# ----------------------------------------------------------------

@app.errorhandler(413)

def request_too_large(_):

    return jsonify({'error': 'Request payload too large.'}), 413





@app.errorhandler(429)

def rate_limit_exceeded(_):

    return jsonify({'error': 'Too many requests. Please wait before trying again.'}), 429





@app.errorhandler(404)

def not_found(_):

    return jsonify({'error': 'Endpoint not found.'}), 404





@app.errorhandler(405)

def method_not_allowed(_):

    return jsonify({'error': 'Method not allowed.'}), 405





# ----------------------------------------------------------------

# Entry point

# ----------------------------------------------------------------

if __name__ == '__main__':

    init_db()

    port       = int(os.environ.get('PORT', 5000))

    debug_mode = os.environ.get('FLASK_ENV', 'production') == 'development'

    app.run(host='0.0.0.0', port=port, debug=debug_mode)