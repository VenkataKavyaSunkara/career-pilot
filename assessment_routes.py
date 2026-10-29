from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from utils.decorators import login_required
from models.assessment_model import AssessmentModel
from models.recommendation_model import RecommendationModel
from models.skill_model import SkillModel
from services.career_recommendation import CareerRecommendationService

assessment_bp = Blueprint('assessment', __name__, url_prefix='/assessment')

# Standardized questionnaire questions dataset
ASSESSMENT_QUESTIONS = [
    {
        'id': 'preferred_domain',
        'title': '1. Which technology or career domain excites you the most?',
        'description': 'Select the core domain you envision working in for your career.',
        'options': [
            ('data_analytics', 'Data Analytics & Business Intelligence (Uncovering patterns, metrics, dashboards)'),
            ('python_programming', 'Python Engineering & Automation (Backend scripting, data workflows, APIs)'),
            ('software_engineering', 'Software Engineering & Core Systems (Desktop/enterprise algorithms, architecture)'),
            ('web_development', 'Full-Stack Web Development (Interactive modern websites, frontend & backend)'),
            ('machine_learning', 'Machine Learning & Artificial Intelligence (Predictive models, deep learning)'),
            ('cybersecurity', 'Cybersecurity & Defensive Operations (Pen testing, threat detection, infosec)'),
            ('ui_ux_design', 'UI/UX & Product Design (Wireframes, intuitive design systems, prototyping)'),
            ('business_systems', 'Business Analysis & Strategy (Requirements gathering, Agile workflows)'),
            ('database_admin', 'Database Administration & Architecture (Server optimization, SQL, backups)'),
            ('digital_marketing', 'Digital Marketing & Growth (SEO, analytics, traffic acquisition)')
        ]
    },
    {
        'id': 'work_activity',
        'title': '2. What type of daily work activity gives you the greatest satisfaction?',
        'description': 'Consider what tasks you naturally enjoy doing for hours.',
        'options': [
            ('coding_logic', 'Writing code, solving algorithmic bugs, and designing logic systems'),
            ('data_number_crunching', 'Working with datasets, numbers, statistical charts, and analytical graphs'),
            ('designing_user_interfaces', 'Designing user layouts, visual hierarchies, color palettes, and mockups'),
            ('security_investigation', 'Auditing networks, checking logs, and hunting security vulnerabilities'),
            ('business_communication', 'Communicating with stakeholders, documenting specs, and managing sprints'),
            ('marketing_strategy', 'Optimizing search visibility, writing content, and tracking conversion funnels')
        ]
    },
    {
        'id': 'analytical_preference',
        'title': '3. How would you describe your analytical and problem-solving style?',
        'description': 'How do you approach solving challenging problems?',
        'options': [
            ('high', 'Deeply analytical and mathematical — I love breaking down complex abstract equations or logic'),
            ('moderate', 'Balanced — I like practical, engineering-oriented problem-solving and structured methods'),
            ('creative', 'Creative and intuitive — I prefer visual aesthetics, user empathy, and human-centric design')
        ]
    },
    {
        'id': 'work_environment',
        'title': '4. Which work environment do you thrive in?',
        'description': 'Think about how you work best with teams.',
        'options': [
            ('independent_code', 'Deep focus coding sessions with well-defined technical specifications'),
            ('cross_functional', 'Cross-functional collaboration with designers, product leads, and clients'),
            ('consulting', 'Consultative advisory role solving varied business and process roadblocks'),
            ('security_ops', 'High-alert operations ensuring zero downtime and maximum protection')
        ]
    },
    {
        'id': 'learning_focus',
        'title': '5. What is your immediate learning priority for the next 3 to 6 months?',
        'description': 'Where do you want to invest your upskilling time?',
        'options': [
            ('frameworks', 'Mastering popular web and backend frameworks (React, Flask, Django, Node.js)'),
            ('data_sql', 'Mastering Advanced SQL, Power BI, and statistical Python libraries'),
            ('ml_deep_learning', 'Training machine learning models and understanding mathematics of AI'),
            ('security_certs', 'Learning ethical hacking, networking protocols, and security tooling'),
            ('design_systems', 'Building extensive Figma design systems and user research case studies')
        ]
    }
]

@assessment_bp.route('/', methods=['GET', 'POST'])
@login_required
def take_assessment():
    """Take career guidance assessment."""
    user_id = session.get('user_id')

    if request.method == 'POST':
        responses = {}
        for q in ASSESSMENT_QUESTIONS:
            val = request.form.get(q['id'])
            if not val:
                flash(f"Please answer question: '{q['title']}'", "warning")
                return render_template('assessment.html', questions=ASSESSMENT_QUESTIONS, responses=request.form)
            responses[q['id']] = val

        # Save assessment to database
        assessment_id = AssessmentModel.create(user_id, responses)

        # Calculate recommendations via Rule-Based Service
        recommendations = CareerRecommendationService.evaluate(user_id, responses)

        # Save recommendations to database
        RecommendationModel.save_batch(user_id, assessment_id, recommendations)

        flash("Assessment successfully evaluated! Here are your personalized career recommendations.", "success")
        return redirect(url_for('careers.recommendations'))

    return render_template('assessment.html', questions=ASSESSMENT_QUESTIONS, responses={})


@assessment_bp.route('/history')
@login_required
def history():
    """View past assessment submissions and recommendation milestones."""
    user_id = session.get('user_id')
    assessments = AssessmentModel.get_user_history(user_id)
    return render_template('history.html', assessments=assessments)


@assessment_bp.route('/history/<int:assessment_id>')
@login_required
def view_past_assessment(assessment_id):
    """View specific past assessment and associated recommendations."""
    user_id = session.get('user_id')
    assessment = AssessmentModel.get_by_id(assessment_id)

    # Ownership check
    if not assessment or assessment['user_id'] != user_id:
        flash("Assessment record not found or access denied.", "danger")
        return redirect(url_for('assessment.history'))

    recommendations = RecommendationModel.get_by_assessment(assessment_id)
    return render_template('recommendations.html', recommendations=recommendations, assessment=assessment)
