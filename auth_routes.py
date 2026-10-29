from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.user_model import UserModel
from models.profile_model import ProfileModel
from utils.security import hash_password, check_password, is_safe_url
from utils.validators import validate_registration

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Student and user registration."""
    if 'user_id' in session:
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        # Validation
        is_valid, error_msg = validate_registration(full_name, email, password, confirm_password)
        if not is_valid:
            flash(error_msg, 'danger')
            return render_template('register.html', full_name=full_name, email=email)

        # Duplicate email check
        existing_user = UserModel.get_by_email(email)
        if existing_user:
            flash("An account with this email address already exists. Please log in.", "warning")
            return redirect(url_for('auth.login'))

        # Secure password hashing with Werkzeug
        p_hash = hash_password(password)
        user_id = UserModel.create(full_name, email, p_hash, role='student')

        # Initialize student profile record
        ProfileModel.upsert(user_id, {
            'education_level': 'Undergraduate',
            'degree': 'Computer Science / Engineering',
            'specialization': 'General',
            'graduation_year': 2026,
            'experience_level': 'Fresher (0-1 yrs)',
            'preferred_location': 'Remote / Flexible',
            'career_interests': '',
            'career_goals': ''
        })

        # Auto-login upon registration
        session.clear()
        session['user_id'] = user_id
        session['user_name'] = full_name
        session['user_email'] = email
        session['user_role'] = 'student'

        flash(f"Welcome to Career Pilot, {full_name}! Your account has been created successfully.", "success")
        return redirect(url_for('main.dashboard'))

    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User and Administrator authentication."""
    if 'user_id' in session:
        return redirect(url_for('main.dashboard'))

    next_url = request.args.get('next')

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        next_page = request.form.get('next') or request.args.get('next')

        if not email or not password:
            flash("Please enter both email address and password.", "danger")
            return render_template('login.html', email=email, next=next_page)

        user = UserModel.get_by_email(email)

        if not user or not check_password(user['password_hash'], password):
            flash("Invalid email or password. Please verify and try again.", "danger")
            return render_template('login.html', email=email, next=next_page)

        # Establish secure session
        session.clear()
        session['user_id'] = user['id']
        session['user_name'] = user['full_name']
        session['user_email'] = user['email']
        session['user_role'] = user['role']

        flash(f"Welcome back, {user['full_name']}!", "success")

        if next_page and is_safe_url(next_page):
            return redirect(next_page)

        if user['role'] == 'admin':
            return redirect(url_for('admin.dashboard'))
        return redirect(url_for('main.dashboard'))

    return render_template('login.html', next=next_url)


@auth_bp.route('/logout')
def logout():
    """Clears user session and logs out."""
    user_name = session.get('user_name', 'Student')
    session.clear()
    flash(f"You have been successfully logged out. See you soon, {user_name}!", "info")
    return redirect(url_for('auth.login'))
