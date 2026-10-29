from flask import Blueprint, render_template, session, redirect, url_for
from utils.decorators import login_required
from models.career_model import CareerModel
from models.profile_model import ProfileModel
from models.recommendation_model import RecommendationModel
from models.job_model import JobModel
from models.roadmap_model import RoadmapModel
from models.assessment_model import AssessmentModel
from services.job_recommendation import JobRecommendationService

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Landing Home Page."""
    careers = CareerModel.get_all(active_only=True)
    featured_careers = careers[:6] if careers else []
    return render_template('index.html', careers=featured_careers)


@main_bp.route('/about')
def about():
    """About Page explaining project goals, methodology, and college mini-project context."""
    return render_template('about.html')


@main_bp.route('/dashboard')
@login_required
def dashboard():
    """Personalized Student Dashboard."""
    user_id = session.get('user_id')
    profile = ProfileModel.get_by_user_id(user_id) or {}
    completion_percentage = ProfileModel.calculate_completion(user_id)

    # Latest recommendations
    recommendations = RecommendationModel.get_latest_by_user(user_id, limit=3)

    # Top recommended jobs
    recommended_jobs = JobRecommendationService.recommend_for_user(user_id, limit=4)

    # Saved jobs
    saved_jobs = JobModel.get_saved_by_user(user_id)

    # Saved roadmaps
    saved_roadmaps = RoadmapModel.get_user_saved_roadmaps(user_id)

    # Assessment history
    assessments = AssessmentModel.get_user_history(user_id)

    return render_template(
        'dashboard.html',
        profile=profile,
        completion_percentage=completion_percentage,
        recommendations=recommendations,
        recommended_jobs=recommended_jobs,
        saved_jobs=saved_jobs,
        saved_roadmaps=saved_roadmaps,
        assessments=assessments
    )
