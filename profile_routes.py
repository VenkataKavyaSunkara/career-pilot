from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from utils.decorators import login_required
from models.profile_model import ProfileModel
from models.skill_model import SkillModel
from utils.validators import validate_profile_data

profile_bp = Blueprint('profile', __name__, url_prefix='/profile')

@profile_bp.route('/', methods=['GET', 'POST'])
@login_required
def view_profile():
    """View and update student profile information and skills inventory."""
    user_id = session.get('user_id')

    if request.method == 'POST':
        form_data = {
            'education_level': request.form.get('education_level', '').strip(),
            'degree': request.form.get('degree', '').strip(),
            'specialization': request.form.get('specialization', '').strip(),
            'graduation_year': request.form.get('graduation_year', '').strip(),
            'experience_level': request.form.get('experience_level', '').strip(),
            'preferred_location': request.form.get('preferred_location', '').strip(),
            'career_interests': request.form.get('career_interests', '').strip(),
            'career_goals': request.form.get('career_goals', '').strip()
        }

        is_valid, err_msg = validate_profile_data(form_data)
        if not is_valid:
            flash(err_msg, "danger")
        else:
            ProfileModel.upsert(user_id, form_data)

            # Sync selected skills if submitted
            selected_skills = request.form.getlist('skills')
            if selected_skills:
                SkillModel.sync_user_skills(user_id, selected_skills)

            flash("Your profile and skills have been updated successfully!", "success")
            return redirect(url_for('profile.view_profile'))

    profile = ProfileModel.get_by_user_id(user_id) or {}
    user_skills = SkillModel.get_user_skills(user_id)
    user_skill_ids = set(s['id'] for s in user_skills)
    skills_by_category = SkillModel.get_by_category()
    completion_percentage = ProfileModel.calculate_completion(user_id)

    return render_template(
        'profile.html',
        profile=profile,
        user_skills=user_skills,
        user_skill_ids=user_skill_ids,
        skills_by_category=skills_by_category,
        completion_percentage=completion_percentage
    )


@profile_bp.route('/skills/add', methods=['POST'])
@login_required
def add_skill():
    """Adds a single skill with chosen proficiency level."""
    user_id = session.get('user_id')
    skill_id = request.form.get('skill_id')
    proficiency = request.form.get('proficiency_level', 'Intermediate')

    if skill_id:
        SkillModel.add_user_skill(user_id, int(skill_id), proficiency)
        flash("Skill added to your profile!", "success")
    return redirect(url_for('profile.view_profile'))


@profile_bp.route('/skills/remove/<int:skill_id>', methods=['POST'])
@login_required
def remove_skill(skill_id):
    """Removes a skill from student profile."""
    user_id = session.get('user_id')
    SkillModel.remove_user_skill(user_id, skill_id)
    flash("Skill removed from your profile.", "info")
    return redirect(url_for('profile.view_profile'))
