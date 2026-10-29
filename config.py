import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base application configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default-dev-secret-key-career-pilot-99')
    
    # Database Settings
    DB_TYPE = os.environ.get('DB_TYPE', 'mysql').lower() # 'mysql' or 'sqlite'
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_PORT = int(os.environ.get('DB_PORT', 3306))
    DB_NAME = os.environ.get('DB_NAME', 'career_pilot')
    DB_USER = os.environ.get('DB_USER', 'root')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', '')
    SQLITE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'career_pilot_local.db')

    # Session Security Settings
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    
    # Recommendation Weights and Tuning
    CAREER_MATCH_THRESHOLD = 30 # Minimum percent match to display
    TOP_CAREERS_LIMIT = 5
    TOP_JOBS_LIMIT = 10


class DevelopmentConfig(Config):
    """Development environment configuration."""
    DEBUG = True
    TESTING = False


class TestingConfig(Config):
    """Testing environment configuration."""
    DEBUG = False
    TESTING = True
    DB_TYPE = 'sqlite'
    SQLITE_PATH = ':memory:'
    SECRET_KEY = 'test-secret-key-for-automated-tests'


class ProductionConfig(Config):
    """Production environment configuration."""
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True


config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
