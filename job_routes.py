from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from utils.decorators import login_required
from models.job_model import JobModel
from models.skill_model import SkillModel
from services.job_recommendation import JobRecommendationService

job_bp = Blueprint('jobs', __name__, url_prefix='/jobs')

@job_bp.route('/')
def list_jobs():
    """Browse, search, and filter demonstration job listings."""
    keyword = request.args.get('keyword', '').strip()
    location = request.args.get('location', '').strip()
    experience = request.args.get('experience', '').strip()
    employment_type = request.args.get('employment_type', '').strip()
    skill_id = request.args.get('skill_id', '').strip()

    if any([keyword, location, experience, employment_type, skill_id]):
        jobs = JobModel.filter_jobs(keyword, location, experience, employment_type, skill_id)
    else:
        jobs = JobModel.get_all(active_only=True)

    # Attach skills & saved status to each job
    user_id = session.get('user_id')
    saved_ids = set()
    if user_id:
        saved = JobModel.get_saved_by_user(user_id)
        saved_ids = set(j['id'] for j in saved)

    for job in jobs:
        job['skills'] = JobModel.get_skills(job['id'])
        job['is_saved'] = job['id'] in saved_ids

    all_skills = SkillModel.get_all()

    return render_template(
        'jobs.html',
        jobs=jobs,
        all_skills=all_skills,
        keyword=keyword,
        location=location,
        experience=experience,
        employment_type=employment_type,
        skill_id=skill_id
    )


@job_bp.route('/<int:job_id>')
def job_detail(job_id):
    """View detailed information about a demonstration job listing."""
    job = JobModel.get_by_id(job_id)
    if not job:
        flash("Job listing not found.", "warning")
        return redirect(url_for('jobs.list_jobs'))

    job_skills = JobModel.get_skills(job_id)
    user_id = session.get('user_id')
    is_saved = JobModel.is_saved(user_id, job_id) if user_id else False

    # Calculate match details if user is logged in
    match_info = None
    if user_id:
        recommended = JobRecommendationService.recommend_for_user(user_id, limit=50)
        for rj in recommended:
            if rj['id'] == job_id:
                match_info = rj
                break

    return render_template(
        'job_detail.html',
        job=job,
        job_skills=job_skills,
        is_saved=is_saved,
        match_info=match_info
    )


@job_bp.route('/save/<int:job_id>', methods=['POST'])
@login_required
def save_job(job_id):
    """Bookmarks a job listing for the student."""
    user_id = session.get('user_id')
    JobModel.save_bookmark(user_id, job_id)
    flash("Job bookmarked successfully!", "success")
    next_url = request.referrer or url_for('jobs.list_jobs')
    return redirect(next_url)


@job_bp.route('/unsave/<int:job_id>', methods=['POST'])
@login_required
def unsave_job(job_id):
    """Removes a job listing from bookmarks."""
    user_id = session.get('user_id')
    JobModel.remove_bookmark(user_id, job_id)
    flash("Job removed from bookmarks.", "info")
    next_url = request.referrer or url_for('jobs.saved_jobs')
    return redirect(next_url)


@job_bp.route('/saved')
@login_required
def saved_jobs():
    """Displays all bookmarked demonstration jobs for the logged in student."""
    user_id = session.get('user_id')
    jobs = JobModel.get_saved_by_user(user_id)
    for j in jobs:
        j['skills'] = JobModel.get_skills(j['id'])
        j['is_saved'] = True
    return render_template('saved_jobs.html', jobs=jobs)


@job_bp.route('/recommended')
@login_required
def recommended_jobs():
    """Shows personalized job recommendations ranked by profile & skill fit."""
    user_id = session.get('user_id')
    jobs = JobRecommendationService.recommend_for_user(user_id, limit=20)
    for j in jobs:
        j['skills'] = JobModel.get_skills(j['id'])
    return render_template('jobs.html', jobs=jobs, is_recommended_view=True)
