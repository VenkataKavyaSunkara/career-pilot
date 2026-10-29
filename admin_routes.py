from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from utils.decorators import admin_required
from models.admin_model import AdminModel
from models.career_model import CareerModel
from models.job_model import JobModel
from models.skill_model import SkillModel
from utils.validators import validate_career_data, validate_job_data

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
@admin_required
def dashboard():
    """Admin Overview Dashboard."""
    stats = AdminModel.get_system_stats()
    audit_logs = AdminModel.get_audit_logs(limit=25)
    return render_template('admin_dashboard.html', stats=stats, audit_logs=audit_logs)


@admin_bp.route('/careers')
@admin_required
def manage_careers():
    """Manage career profiles."""
    careers = CareerModel.get_all(active_only=False)
    skills = SkillModel.get_all()
    return render_template('manage_careers.html', careers=careers, skills=skills)


@admin_bp.route('/careers/add', methods=['POST'])
@admin_required
def add_career():
    """Create a new career profile."""
    admin_id = session.get('user_id')
    data = {
        'title': request.form.get('title', '').strip(),
        'description': request.form.get('description', '').strip(),
        'required_education': request.form.get('required_education', '').strip(),
        'entry_level_roles': request.form.get('entry_level_roles', '').strip(),
        'is_active': 1 if request.form.get('is_active') == '1' else 0
    }

    is_valid, err = validate_career_data(data)
    if not is_valid:
        flash(err, 'danger')
        return redirect(url_for('admin.manage_careers'))

    career_id = CareerModel.create(
        data['title'],
        data['description'],
        data['required_education'],
        data['entry_level_roles'],
        data['is_active']
    )

    AdminModel.log_audit(admin_id, 'CREATE_CAREER', 'career', career_id, f"Added career: {data['title']}")
    flash(f"Career profile '{data['title']}' created successfully!", "success")
    return redirect(url_for('admin.manage_careers'))


@admin_bp.route('/careers/toggle/<int:career_id>', methods=['POST'])
@admin_required
def toggle_career(career_id):
    """Toggle career active/inactive state."""
    admin_id = session.get('user_id')
    career = CareerModel.get_by_id(career_id)
    if career:
        new_status = not bool(career['is_active'])
        CareerModel.toggle_active(career_id, new_status)
        AdminModel.log_audit(admin_id, 'TOGGLE_CAREER', 'career', career_id, f"Set active={new_status}")
        flash(f"Career '{career['title']}' status updated to {'Active' if new_status else 'Inactive'}.", "info")
    return redirect(url_for('admin.manage_careers'))


@admin_bp.route('/jobs')
@admin_required
def manage_jobs():
    """Manage demonstration job listings."""
    jobs = JobModel.get_all(active_only=False, limit=100)
    skills = SkillModel.get_all()
    return render_template('manage_jobs.html', jobs=jobs, skills=skills)


@admin_bp.route('/jobs/add', methods=['POST'])
@admin_required
def add_job():
    """Create a demonstration job listing."""
    admin_id = session.get('user_id')
    data = {
        'title': request.form.get('title', '').strip(),
        'company_name': request.form.get('company_name', '').strip(),
        'description': request.form.get('description', '').strip(),
        'required_education': request.form.get('required_education', '').strip(),
        'experience_level': request.form.get('experience_level', '').strip(),
        'location': request.form.get('location', '').strip(),
        'employment_type': request.form.get('employment_type', '').strip(),
        'application_url': request.form.get('application_url', '').strip() or 'https://example.com/demo-careers',
        'is_active': 1 if request.form.get('is_active') == '1' else 0
    }

    is_valid, err = validate_job_data(data)
    if not is_valid:
        flash(err, 'danger')
        return redirect(url_for('admin.manage_jobs'))

    job_id = JobModel.create(
        data['title'],
        data['company_name'],
        data['description'],
        data['required_education'],
        data['experience_level'],
        data['location'],
        data['employment_type'],
        data['application_url'],
        data['is_active']
    )

    # Sync skills if provided
    selected_skills = request.form.getlist('skills')
    if selected_skills:
        JobModel.sync_skills(job_id, selected_skills)

    AdminModel.log_audit(admin_id, 'CREATE_JOB', 'job', job_id, f"Added job: {data['title']} at {data['company_name']}")
    flash(f"Demonstration job '{data['title']}' added successfully!", "success")
    return redirect(url_for('admin.manage_jobs'))


@admin_bp.route('/jobs/toggle/<int:job_id>', methods=['POST'])
@admin_required
def toggle_job(job_id):
    """Toggle job active/inactive state."""
    admin_id = session.get('user_id')
    job = JobModel.get_by_id(job_id)
    if job:
        new_status = not bool(job['is_active'])
        JobModel.toggle_active(job_id, new_status)
        AdminModel.log_audit(admin_id, 'TOGGLE_JOB', 'job', job_id, f"Set active={new_status}")
        flash(f"Job '{job['title']}' status updated to {'Active' if new_status else 'Inactive'}.", "info")
    return redirect(url_for('admin.manage_jobs'))
