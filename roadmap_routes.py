from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from utils.decorators import login_required
from models.roadmap_model import RoadmapModel
from services.roadmap_service import RoadmapService

roadmap_bp = Blueprint('roadmaps', __name__, url_prefix='/roadmaps')

@roadmap_bp.route('/<int:roadmap_id>')
def view_roadmap(roadmap_id):
    """View career learning roadmap with stages, checklist, projects, and interview questions."""
    user_id = session.get('user_id')
    details = RoadmapService.get_roadmap_details(roadmap_id, user_id=user_id)

    if not details:
        flash("Learning roadmap not found.", "warning")
        return redirect(url_for('careers.list_careers'))

    return render_template('roadmap.html', **details)


@roadmap_bp.route('/career/<int:career_id>')
def view_by_career(career_id):
    """Navigates to the roadmap tied to a specific career."""
    roadmap = RoadmapModel.get_by_career_id(career_id)
    if not roadmap:
        flash("A learning roadmap is being crafted for this career. Check back soon!", "info")
        return redirect(url_for('careers.career_detail', career_id=career_id))
    return redirect(url_for('roadmaps.view_roadmap', roadmap_id=roadmap['id']))


@roadmap_bp.route('/enroll/<int:roadmap_id>', methods=['POST'])
@login_required
def enroll(roadmap_id):
    """Enrolls the student in this learning roadmap."""
    user_id = session.get('user_id')
    RoadmapModel.enroll_user(user_id, roadmap_id)
    flash("Successfully added this learning roadmap to your active goals!", "success")
    return redirect(url_for('roadmaps.view_roadmap', roadmap_id=roadmap_id))


@roadmap_bp.route('/toggle-step', methods=['POST'])
@login_required
def toggle_step():
    """Toggles checklist step completion status and updates student progress."""
    user_id = session.get('user_id')
    roadmap_id = request.form.get('roadmap_id')
    step_name = request.form.get('step_name')
    is_completed = request.form.get('is_completed') in ('true', '1', 'on')

    if roadmap_id and step_name:
        RoadmapModel.toggle_step(user_id, int(roadmap_id), step_name, is_completed)
        flash(f"Checklist updated: '{step_name}'", "info")

    next_url = request.referrer or url_for('roadmaps.view_roadmap', roadmap_id=roadmap_id)
    return redirect(next_url)
