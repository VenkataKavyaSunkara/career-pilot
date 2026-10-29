import os
import secrets
from flask import session, request, abort, current_app

class CSRFProtect:
    """
    Lightweight, robust CSRF protection extension for Flask.
    Generates and validates session-tied anti-CSRF tokens for state-changing HTTP methods.
    """
    def __init__(self, app=None):
        self.exempt_views = set()
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        # Register context processor so templates can use {{ csrf_token() }}
        @app.context_processor
        def inject_csrf_token():
            return dict(csrf_token=self.generate_csrf_token)

        # Before request hook to validate CSRF token on unsafe methods
        @app.before_request
        def check_csrf():
            if request.method in ('GET', 'HEAD', 'OPTIONS', 'TRACE'):
                return
            
            # Allow testing bypass if configured
            if current_app.config.get('TESTING', False) and not current_app.config.get('WTF_CSRF_ENABLED', False):
                return
            
            # Check view exemptions
            if request.endpoint and request.endpoint in self.exempt_views:
                return

            sent_token = (
                request.form.get('csrf_token') or 
                request.headers.get('X-CSRFToken') or 
                request.headers.get('X-CSRF-Token')
            )
            stored_token = session.get('_csrf_token')

            if not stored_token or not sent_token or not secrets.compare_digest(stored_token, sent_token):
                # Reject invalid CSRF token
                abort(400, description="CSRF validation failed. Invalid or missing CSRF token.")

    def generate_csrf_token(self):
        """Generates or retrieves the current session CSRF token."""
        if '_csrf_token' not in session:
            session['_csrf_token'] = secrets.token_hex(32)
        return session['_csrf_token']

    def exempt(self, view_func):
        """Decorator to mark a view as exempt from CSRF checks."""
        self.exempt_views.add(view_func.__name__)
        return view_func

csrf = CSRFProtect()
