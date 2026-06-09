"""
MARENA-HUB  –  Unified Flask Application
=========================================
Consolidates all fragmented backend scripts into a single server.
Run:  python backend/app.py
"""

from flask import (
    Flask, render_template, render_template_string, request, redirect,
    url_for, session, send_from_directory, jsonify, flash
)
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ──────────────────────────────────────
# App setup
# ──────────────────────────────────────

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)

app = Flask(
    __name__,
    template_folder=os.path.join(PROJECT_DIR, 'templates'),
    static_folder=os.path.join(PROJECT_DIR, 'static'),
)
app.secret_key = 'marena_hub_secure_session_key'

# ──────────────────────────────────────
# In-memory user database (volatile)
# ──────────────────────────────────────

DATABASE = {}


# Configuration
YOUR_EMAIL = "marenahubofficial@gmail.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465
SENDER_EMAIL = os.environ.get("MAIL_SENDER", "marenahubofficial@gmail.com")
# Use a real Gmail App Password for the sender account above.
SENDER_PASSWORD = os.environ.get("MAIL_PASSWORD", "belddwykwwdcctau")

def send_email_notification(user_name, user_email, subject, message_body):
    """Send contact form contents via email, with a local fallback if SMTP fails."""
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['Reply-To'] = user_email
        msg['To'] = YOUR_EMAIL
        msg['Subject'] = f"[MARENA-HUB Contact] {subject}"

        body_content = f"""
        New Contact Form Submission from MARENA-HUB:
        --------------------------------------------------
        From: {user_name}
        User's Email: {user_email}
        Subject: {subject}

        Message:
        {message_body}
        --------------------------------------------------
        """
        msg.attach(MIMEText(body_content, 'plain'))

        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        new_func(e)
        try:
            with open(CONTACT_FILE, 'a', encoding='utf-8') as f:
                f.write(f"{user_name}|{user_email}|{subject}|{message_body}\n")
        except Exception:
            pass
        return True

def new_func(e):
    print(f"Email error: {e}")


# ──────────────────────────────────────
# Data files – all stored in backend/
# ──────────────────────────────────────

SCORE_FILES = {
    'python':  os.path.join(BASE_DIR, 'python_scores.txt'),
    'html':    os.path.join(BASE_DIR, 'html_scores.txt'),
    'css':     os.path.join(BASE_DIR, 'css_scores.txt'),
    'js':      os.path.join(BASE_DIR, 'js_scores.txt'),
}

# Also read legacy data files if they exist
LEGACY_SCORE_FILES = [
    os.path.join(BASE_DIR, 'data.txt'),
    os.path.join(BASE_DIR, 'data(1).txt'),
    os.path.join(BASE_DIR, 'htmldata.txt'),
    os.path.join(PROJECT_DIR, 'data.txt'),
]

FEEDBACK_FILE = os.path.join(BASE_DIR, 'feedback.txt')
CONTACT_FILE = os.path.join(BASE_DIR, 'contact_messages.txt')

# Create score files if they don't exist
for path in SCORE_FILES.values():
    if not os.path.exists(path):
        open(path, 'w').close()

if not os.path.exists(FEEDBACK_FILE):
    open(FEEDBACK_FILE, 'w').close()

if not os.path.exists(CONTACT_FILE):
    open(CONTACT_FILE, 'w').close()



# Map course names to their quiz template files
COURSE_TEMPLATES = {
    'python': 'quiz1.html',
    'html':   'quiz2.html',
    'css':    'quiz3.html',
    'js':     'quiz4.html',
}


# ═══════════════════════════════════════
#  HELPER FUNCTIONS
# ═══════════════════════════════════════

def read_scores_from_file(filepath):
    """Read name,score lines from a text file. Returns list of dicts."""
    data = []
    if not os.path.exists(filepath):
        return data
    try:
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or ',' not in line:
                    continue
                parts = line.split(',', 1)
                name = parts[0].strip()
                score_str = parts[1].strip()
                if score_str.isdigit():
                    data.append({'username': name, 'score': int(score_str)})
    except Exception:
        pass
    return data




# ═══════════════════════════════════════
#  PAGE ROUTES
# ═══════════════════════════════════════

@app.route('/')
def index():
    """Login page (home)."""
    return render_template('index.html')


@app.route('/home')
@app.route('/Home.html')
def home():
    return render_template('Home.html')




# ─── Video Pages ──────────────────────

@app.route('/video1')
@app.route('/video1.html')
def video1():
    return render_template('video1.html')


@app.route('/video2')
@app.route('/video2.html')
def video2():
    return render_template('video2.html')


@app.route('/video3')
@app.route('/video3.html')
def video3():
    return render_template('video3.html')


@app.route('/video4')
@app.route('/video4.html')
def video4():
    return render_template('video4.html')


# Legacy quiz.html – redirect based on Referer
@app.route('/quiz.html')
def quiz_redirect():
    referer = request.headers.get('Referer', '')
    if 'video1' in referer:
        return redirect('/quiz/python')
    elif 'video2' in referer:
        return redirect('/quiz/html')
    elif 'video3' in referer:
        return redirect('/quiz/js')
    elif 'video4' in referer:
        return redirect('/quiz/css')
    # Default to python quiz
    return redirect('/quiz/python')


# ─── Certificate Pages ───────────────

@app.route('/certificate1')
@app.route('/certificate1.html')
def certificate1():
    return render_template('certificate1.html')


@app.route('/certificate2')
@app.route('/certificate2.html')
def certificate2():
    return render_template('certificate2.html')


@app.route('/certificate3')
@app.route('/certificate3.html')
def certificate3():
    return render_template('certificate3.html')


@app.route('/certificate4')
@app.route('/certificate4.html')
def certificate4():
    return render_template('certificate4.html')


# Generic /certificate.html redirect
@app.route('/certificate.html')
def certificate_generic():
    return redirect('/certificate1.html')



# ─── Feedback Page ────────────────────

@app.route('/feedback.html')
def feedback_page_alias():
    return render_template('feedback.html')


# ─── Contact Page ─────────────────────



#CONTACT PAGE

# Updated Route to handle both viewing the page and form submission
@app.route('/Contact.html', methods=['GET', 'POST'])
def contact_page_alias():
    if request.method == 'POST':
        # Extract data from the HTML form elements using their 'name' attributes
        user_name = request.form.get('name')
        user_email = request.form.get('email')
        subject = request.form.get('subject')
        message_body = request.form.get('message')

        # Trigger the email function
        success = send_email_notification(user_name, user_email, subject, message_body)
        
        if success:
            flash("Your message has been sent successfully!", "success")
        else:
            flash("There was an error sending your message. Please try again.", "danger")
            
        return redirect(url_for('contact_page_alias'))

    # If it's a GET request, just display the page
    return render_template('Contact.html')

# ─── Auth Pages ───────────────────────

@app.route('/index.html')
def login_page():
    return render_template('index.html')


@app.route('/signup.html')
def signup_page_alias():
    return render_template('signup.html')


@app.route('/forget.html')
def forget_page_alias():
    return render_template('forget.html')


@app.route('/recovery.html')
def recovery_page_alias():
    return render_template('recovery.html')


# Also handle sign.html as a redirect to index (sign out)
@app.route('/sign.html')
def signout_redirect():
    session.pop('logged_in_user', None)
    return redirect('/')


# ═══════════════════════════════════════
#  AUTHENTICATION ROUTES
# ═══════════════════════════════════════


  


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')

    full_name = (request.form.get('fullName') or '').strip()
    email = (request.form.get('email') or '').strip()
    username = (request.form.get('username') or '').strip()
    password = (request.form.get('password') or '').strip()
    confirm = (request.form.get('confirmPassword') or '').strip()

    if confirm != password:
        return render_template('signup.html')

    generated_username = email.split('@')[0].lower() if email else 'student'

    DATABASE[email] = {
        'name': full_name,
        'email': email,
        'username': username or generated_username,
        'password': password,
    }

    session['logged_in_user'] = email
    return redirect('/home')


@app.route('/forget', methods=['GET', 'POST'])
def forget():
    if request.method == 'GET':
        return render_template('forget.html')

    email = (request.form.get('email') or '').strip()
    if email:
        return f"""
        <h2>Reset link has been sent to {email}</h2>
        <a href="/">Go Back</a>
        """
    return """
    <h2>Please enter your email address</h2>
    <a href="/">Go Back</a>
    """


@app.route('/recovery', methods=['GET', 'POST'])
def recovery():
    if request.method == 'GET':
        return render_template('recovery.html')

    password = (request.form.get('password') or '').strip()
    confirm = (request.form.get('confirmPassword') or '').strip()

    if password and password == confirm:
        return """
        <h2>Password has been reset successfully!</h2>
        <a href="/">Sign In</a>
        """
    return """
    <h2>Passwords do not match. Try again.</h2>
    <a href="/recovery">Go Back</a>
    """

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('index.html')

    username = (request.form.get('username') or '').strip()
    password = (request.form.get('password') or '').strip()

    for email, user in DATABASE.items():
        if (user.get('username') == username or user.get('name') == username) and user.get('password') == password:
            session['logged_in_user'] = email
            return redirect('/home')

    return render_template('index.html', error='Invalid credentials')

@app.route('/update-profile', methods=['POST'])
def update_profile():
    current_user_email = session.get('logged_in_user')
    if not current_user_email or current_user_email not in DATABASE:
        return redirect('/signup')

    new_name = request.form.get('fullName')
    new_email = request.form.get('email')

    DATABASE[current_user_email]['name'] = new_name

    if new_email and new_email != current_user_email:
        DATABASE[new_email] = DATABASE.pop(current_user_email)
        DATABASE[new_email]['email'] = new_email
        session['logged_in_user'] = new_email

    return redirect('/account')


@app.route('/logout')
def logout():
    session.pop('logged_in_user', None)
    session.pop('student_name', None)
    return redirect('/')



# ═══════════════════════════════════════
#  LEADERBOARD (aggregated)
# ═══════════════════════════════════════

@app.route('/leaderboard')
@app.route('/leaderboard.html')
def leaderboard():
    all_scores = []

    # Read from all course score files
    for filepath in SCORE_FILES.values():
        all_scores.extend(read_scores_from_file(filepath))

    # Read from legacy data files
    for filepath in LEGACY_SCORE_FILES:
        all_scores.extend(read_scores_from_file(filepath))

    # Deduplicate: keep highest score per username
    best = {}
    for entry in all_scores:
        name = entry['username']
        if name not in best or entry['score'] > best[name]:
            best[name] = entry['score']

    data = [{'username': k, 'score': v} for k, v in best.items()]
    data = sorted(data, key=lambda x: x['score'], reverse=True)

    template_path = os.path.join(PROJECT_DIR, 'templates', 'leaderboard.html')
    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()

    sync_script = '''
<script>
(function() {
  const params = new URLSearchParams(window.location.search);
  if (params.has('synced')) {
    return;
  }

  const localScores = JSON.parse(localStorage.getItem('leaderboard') || '[]');
  if (!Array.isArray(localScores) || localScores.length === 0) {
    return;
  }

  const studentName = localStorage.getItem('studentName') || 'Anonymous';
  const payload = localScores.map(item => ({
    quiz: item.quiz || item.course || '',
    score: item.score || 0,
    username: studentName
  }));

  fetch('/sync-scores', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  }).then(response => response.json())
    .then(data => {
      if (data && data.synced) {
        localStorage.removeItem('leaderboard');
        params.set('synced', '1');
        window.location.search = params.toString();
      }
    }).catch(() => {
      // ignore sync errors silently
    });
})();
</script>
'''

    inject_point = template_content.rfind('</body>')
    if inject_point == -1:
        inject_point = template_content.rfind('</html>')
    if inject_point == -1:
        inject_point = len(template_content)

    template_content = template_content[:inject_point] + sync_script + template_content[inject_point:]
    return render_template_string(template_content, leaderboard=data)


@app.route('/sync-scores', methods=['POST'])
def sync_scores():
    entries = request.get_json(silent=True)
    if not isinstance(entries, list):
        return jsonify({'synced': 0}), 400

    synced_count = 0
    for item in entries:
        if not isinstance(item, dict):
            continue

        raw_quiz = str(item.get('quiz') or item.get('course') or '').strip().lower()
        score = item.get('score')
        try:
            score = int(score)
        except (TypeError, ValueError):
            continue

        username = str(item.get('username') or 'Anonymous').strip() or 'Anonymous'
        if 'python' in raw_quiz:
            course = 'python'
        elif 'html' in raw_quiz:
            course = 'html'
        elif 'css' in raw_quiz:
            course = 'css'
        elif 'js' in raw_quiz or 'javascript' in raw_quiz:
            course = 'js'
        else:
            continue

        score_file = SCORE_FILES.get(course)
        if not score_file:
            continue

        try:
            with open(score_file, 'a', encoding='utf-8') as f:
                f.write(f'{username},{score}\n')
            synced_count += 1
        except Exception:
            continue

    return jsonify({'synced': synced_count})


# ══════════════════════════════════════
#  FEEDBACK
# ═══════════════════════════════════════

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'GET':
        return render_template('feedback.html')

    name = (request.form.get('name') or '').strip()
    email = (request.form.get('email') or '').strip()
    rating = (request.form.get('rating') or '0').strip()
    message = (request.form.get('message') or '').strip()

    with open(FEEDBACK_FILE, 'a') as f:
        f.write(f'{name}|{email}|{rating}|{message}\n')

    return """
    <div style="text-align:center; margin-top:60px; font-family:sans-serif;">
        <h1>Thank You for Your Feedback!</h1>
        <p>We appreciate your time and thoughts.</p>
       <botton> <a href="/home" style="color:#blue; font-size:25px;">Back to Home</a></botton>
    </div>
    """


# ═══════════════════════════════════════
#  CONTACT FORM
# ═══════════════════════════════════════

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'GET':
        return render_template('Contact.html')

    name = (request.form.get('name') or '').strip()
    email = (request.form.get('email') or '').strip()
    subject = (request.form.get('subject') or '').strip()
    message = (request.form.get('message') or '').strip()

    success = send_email_notification(name, email, subject, message)

    if success:
        return """
        <div style="text-align:center; margin-top:60px; font-family:sans-serif;">
            <h1>Message Sent Successfully!</h1>
            <p>Thank you for reaching out to MARENA-HUB.</p>
            <a href="/home" style="color:#0a1a33; font-size:18px;">Back to Home</a>
        </div>
        """
    return """
    <div style="text-align:center; margin-top:60px; font-family:sans-serif;">
        <h1>System Error</h1>
        <p>We could not send your message at this time. Please try again later.</p>
        <a href="/contact" style="color:#0a1a33; font-size:18px;">Try Again</a>
    </div>
    """, 500


# Simple structural layout expected for your user dictionary
# DATABASE = {
#     "user@gmail.com": {
#         "name": "User Name",
#         "email": "user@gmail.com",
#         "password": "hashed_or_plain_password"
#     }
# }

@app.route('/account', methods=['GET', 'POST'])
@app.route('/account.html', methods=['GET', 'POST'])
@app.route('/Account.html', methods=['GET', 'POST'])
def account_page():
    email = session.get('logged_in_user')
    
    # Send user back to the login page if they aren't logged in
    if not email or email not in DATABASE:
        flash("Please log in to access your dashboard.", "danger")
        return redirect(url_for('login_page'))  # Replace with your custom login route identifier

    student_data = DATABASE.get(email)
    if not student_data:
        student_data = {
            'name': email.split('@')[0].replace('.', ' ').title(),
            'email': email,
            'username': email.split('@')[0],
            'password': '',
        }
        DATABASE[email] = student_data

    if request.method == 'POST':
        new_name = request.form.get('fullName')
        new_email = request.form.get('email')
        new_password = request.form.get('password')
        confirm_password = request.form.get('confirmPassword')
        
        # Optional basic password check
        if new_password and new_password != confirm_password:
            flash("Passwords do not match!", "danger")
            return render_template('Account.html', student=student_data)

        # 1. Update Username
        student_data['name'] = new_name
        
        # 2. Update Password if they provided a new one
        if new_password:
            student_data['password'] = new_password 
            
        # 3. Update Email (and re-key the database safely)
        if new_email != email:
            # Shift data over to the new email address key inside the dictionary
            DATABASE[new_email] = DATABASE.pop(email)
            DATABASE[new_email]['email'] = new_email
            session['logged_in_user'] = new_email  # Keep session aligned with their new email
        
        flash("Profile updated successfully!", "success")
        return redirect(url_for('account_page'))

    # GET request: Render template with the authenticated student's data
    return render_template('Account.html', student=student_data)


# ═══════════════════════════════════════
#  FALLBACK ROUTE
#  Handles bare .html links from templates
#  e.g. <a href="home.html"> resolves properly
# ═══════════════════════════════════════

@app.route('/<path:filename>')
def fallback(filename):
    """
    Catch-all route that:
    1. Tries to serve a template if <filename> matches a template file
    2. Tries to serve a static file if it exists in static/
    3. Returns 404 otherwise
    """
    # Check if it's a template file (.html)
    if filename.endswith('.html'):
        template_path = os.path.join(PROJECT_DIR, 'templates', filename)
        if os.path.exists(template_path):
            return render_template(filename)

        # Linux file system is case-sensitive, so resolve common casing variants.
        templates_dir = os.path.join(PROJECT_DIR, 'templates')
        if os.path.isdir(templates_dir):
            lower_filename = filename.lower()
            for entry in os.listdir(templates_dir):
                if entry.lower() == lower_filename:
                    return render_template(entry)

    # Check if it's a static file (CSS, images, etc.)
    static_path = os.path.join(PROJECT_DIR, 'static', filename)
    if os.path.exists(static_path):
        return send_from_directory(os.path.join(PROJECT_DIR, 'static'), filename)

    # Also check templates folder for non-html assets (legacy)
    template_asset = os.path.join(PROJECT_DIR, 'templates', filename)
    if os.path.exists(template_asset):
        return send_from_directory(os.path.join(PROJECT_DIR, 'templates'), filename)

    return f"<h1>404 – Page Not Found</h1><p>{filename} does not exist.</p>", 404

# ═══════════════════════════════════════
#  RUN
# ═══════════════════════════════════════

if __name__ == '__main__':
    print("=" * 50)
    print("  MARENA-HUB  –  Starting Unified Server")
    print(f"  Templates: {app.template_folder}")
    print(f"  Static:    {app.static_folder}")
    print("=" * 50)
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)