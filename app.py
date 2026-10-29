import os
from datetime import datetime
from flask import Flask, render_template
from config import config_by_name
from extensions import csrf
from database.connection import init_db

def create_app(config_name=None):
    """Application Factory Pattern for Career Pilot."""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')

    app = Flask(__name__)
    app.config.from_object(config_by_name.get(config_name, config_by_name['default']))

    # Initialize extensions
    csrf.init_app(app)
    init_db(app)

    # Register custom Jinja2 date formatter filter
    @app.template_filter('format_date')
    def format_date(val, fmt='%b %d, %Y'):
        if not val:
            return 'Recent'
        if hasattr(val, 'strftime'):
            return val.strftime(fmt)
        try:
            # Handles SQLite string timestamp format 'YYYY-MM-DD HH:MM:SS'
            clean_str = str(val).split('.')[0].replace('T', ' ').replace('Z', '')
            dt = datetime.strptime(clean_str, '%Y-%m-%d %H:%M:%S')
            return dt.strftime(fmt)
        except Exception:
            return str(val)[:10]

    # Register Blueprints
    from routes.main_routes import main_bp
    from routes.auth_routes import auth_bp
    from routes.profile_routes import profile_bp
    from routes.assessment_routes import assessment_bp
    from routes.career_routes import career_bp
    from routes.job_routes import job_bp
    from routes.roadmap_routes import roadmap_bp
    from routes.admin_routes import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(assessment_bp)
    app.register_blueprint(career_bp)
    app.register_blueprint(job_bp)
    app.register_blueprint(roadmap_bp)
    app.register_blueprint(admin_bp)

    # Register Global HTTP Error Handlers
    @app.errorhandler(403)
    def forbidden_error(e):
        return render_template('403.html'), 403

    @app.errorhandler(404)
    def not_found_error(e):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(e):
        return render_template('404.html', message="An unexpected error occurred. Please try again."), 500

    return app

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
