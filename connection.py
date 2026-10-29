import os
import sqlite3
from flask import g, current_app

def get_db():
    """
    Get or create a database connection for the current application context.
    Supports both MySQL (primary) and SQLite (testing and offline fallback).
    """
    if '_database' not in g:
        db_type = current_app.config.get('DB_TYPE', 'mysql').lower()

        if db_type == 'mysql':
            try:
                # First attempt using mysql.connector
                import mysql.connector
                g._database = mysql.connector.connect(
                    host=current_app.config.get('DB_HOST', 'localhost'),
                    port=current_app.config.get('DB_PORT', 3306),
                    user=current_app.config.get('DB_USER', 'root'),
                    password=current_app.config.get('DB_PASSWORD', ''),
                    database=current_app.config.get('DB_NAME', 'career_pilot'),
                    charset='utf8mb4',
                    autocommit=False
                )
                g._db_flavor = 'mysql'
            except Exception as e1:
                try:
                    # Fallback to PyMySQL if mysql.connector fails
                    import pymysql
                    import pymysql.cursors
                    g._database = pymysql.connect(
                        host=current_app.config.get('DB_HOST', 'localhost'),
                        port=current_app.config.get('DB_PORT', 3306),
                        user=current_app.config.get('DB_USER', 'root'),
                        password=current_app.config.get('DB_PASSWORD', ''),
                        database=current_app.config.get('DB_NAME', 'career_pilot'),
                        charset='utf8mb4',
                        cursorclass=pymysql.cursors.DictCursor,
                        autocommit=False
                    )
                    g._db_flavor = 'pymysql'
                except Exception as e2:
                    # If MySQL is not running and development fallback is permitted, use SQLite
                    if current_app.config.get('DEBUG') or current_app.config.get('TESTING'):
                        sqlite_path = current_app.config.get('SQLITE_PATH', 'career_pilot_local.db')
                        conn = sqlite3.connect(sqlite_path)
                        conn.row_factory = sqlite3.Row
                        conn.execute("PRAGMA foreign_keys = ON")
                        g._database = conn
                        g._db_flavor = 'sqlite'
                    else:
                        raise RuntimeError(
                            f"Could not connect to MySQL database '{current_app.config.get('DB_NAME')}'. "
                            f"Errors: mysql-connector ({e1}), PyMySQL ({e2}). Please ensure MySQL is running."
                        )
        else:
            # SQLite mode (used primarily for automated test suites)
            sqlite_path = current_app.config.get('SQLITE_PATH', ':memory:')
            conn = sqlite3.connect(sqlite_path)
            conn.row_factory = sqlite3.Row
            conn.execute("PRAGMA foreign_keys = ON")
            g._database = conn
            g._db_flavor = 'sqlite'

    return g._database


def close_db(e=None):
    """Closes the current request's database connection if one exists."""
    db = g.pop('_database', None)
    if db is not None:
        try:
            db.close()
        except Exception:
            pass


def query_db(query, args=(), one=False):
    """
    Execute a parameterized SELECT query and return rows as dictionaries.
    Automatically handles %s -> ? conversion when running in SQLite mode.
    """
    conn = get_db()
    flavor = getattr(g, '_db_flavor', 'mysql')

    if flavor == 'sqlite':
        sqlite_query = query.replace('%s', '?')
        # Also adjust MySQL specific syntax if present
        sqlite_query = sqlite_query.replace('NOW()', "datetime('now')")
        cur = conn.cursor()
        cur.execute(sqlite_query, args)
        rows = [dict(row) for row in cur.fetchall()]
        cur.close()
        return (rows[0] if rows else None) if one else rows

    elif flavor == 'mysql':
        # mysql.connector
        cur = conn.cursor(dictionary=True)
        cur.execute(query, args)
        rows = cur.fetchall()
        cur.close()
        return (rows[0] if rows else None) if one else rows

    elif flavor == 'pymysql':
        with conn.cursor() as cur:
            cur.execute(query, args)
            rows = cur.fetchall()
            return (rows[0] if rows else None) if one else rows


def execute_db(query, args=(), commit=True):
    """
    Execute an INSERT, UPDATE, or DELETE query.
    Returns the lastrowid or affected rows.
    """
    conn = get_db()
    flavor = getattr(g, '_db_flavor', 'mysql')

    if flavor == 'sqlite':
        sqlite_query = query.replace('%s', '?')
        sqlite_query = sqlite_query.replace('NOW()', "datetime('now')")
        # Replace ON DUPLICATE KEY UPDATE with SQLite syntax if any
        if 'ON DUPLICATE KEY UPDATE' in sqlite_query:
            sqlite_query = sqlite_query.split('ON DUPLICATE KEY UPDATE')[0]
        cur = conn.cursor()
        cur.execute(sqlite_query, args)
        last_id = cur.lastrowid
        if commit:
            conn.commit()
        cur.close()
        return last_id

    elif flavor == 'mysql':
        cur = conn.cursor()
        cur.execute(query, args)
        last_id = cur.lastrowid
        if commit:
            conn.commit()
        cur.close()
        return last_id

    elif flavor == 'pymysql':
        with conn.cursor() as cur:
            cur.execute(query, args)
            last_id = cur.lastrowid
            if commit:
                conn.commit()
            return last_id


def init_db(app):
    """Registers teardown handlers with the Flask application."""
    app.teardown_appcontext(close_db)
