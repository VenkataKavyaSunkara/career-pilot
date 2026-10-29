import os
import sys
import re

# Ensure parent directory is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv

load_dotenv()

def run_init_db():
    """Initializes the MySQL or SQLite database using schema.sql and seed_data.sql."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    schema_path = os.path.join(base_dir, 'schema.sql')
    seed_path = os.path.join(base_dir, 'seed_data.sql')

    with open(schema_path, 'r', encoding='utf-8') as f:
        schema_sql = f.read()

    with open(seed_path, 'r', encoding='utf-8') as f:
        seed_sql = f.read()

    db_type = os.environ.get('DB_TYPE', 'mysql').lower()

    if db_type == 'mysql':
        try:
            import mysql.connector
            conn = mysql.connector.connect(
                host=os.environ.get('DB_HOST', 'localhost'),
                port=int(os.environ.get('DB_PORT', 3306)),
                user=os.environ.get('DB_USER', 'root'),
                password=os.environ.get('DB_PASSWORD', '')
            )
            cursor = conn.cursor()
            db_name = os.environ.get('DB_NAME', 'career_pilot')
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
            cursor.execute(f"USE `{db_name}`;")

            for statement in schema_sql.split(';'):
                stmt = statement.strip()
                if stmt:
                    cursor.execute(stmt)

            for statement in seed_sql.split(';'):
                stmt = statement.strip()
                if stmt:
                    cursor.execute(stmt)

            conn.commit()
            cursor.close()
            conn.close()
            print(f"[SUCCESS] MySQL database '{db_name}' initialized successfully with schema and seed data!")
            return True

        except Exception as e:
            print(f"[WARNING] MySQL connection failed: {e}")
            print("[INFO] Setting up local SQLite database fallback for development/testing...")
            db_type = 'sqlite'

    if db_type == 'sqlite':
        import sqlite3
        sqlite_file = os.path.join(os.path.dirname(base_dir), 'career_pilot_local.db')
        conn = sqlite3.connect(sqlite_file)
        cur = conn.cursor()

        # Transform schema.sql for SQLite compatibility
        clean_schema = schema_sql.replace('INT AUTO_INCREMENT PRIMARY KEY', 'INTEGER PRIMARY KEY AUTOINCREMENT')
        clean_schema = clean_schema.replace('ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci', '')
        clean_schema = clean_schema.replace('ON UPDATE CURRENT_TIMESTAMP', '')
        clean_schema = re.sub(r'UNIQUE KEY\s+[a-zA-Z0-9_]+', 'UNIQUE', clean_schema)

        for statement in clean_schema.split(';'):
            stmt = statement.strip()
            if not stmt:
                continue
            lines = [l for l in stmt.split('\n') if not l.strip().startswith('INDEX ') and not l.strip().startswith('KEY ')]
            # Clean trailing comma before closing parenthesis
            for i in range(len(lines) - 1, -1, -1):
                if lines[i].strip().startswith(')'):
                    for j in range(i - 1, -1, -1):
                        if lines[j].strip():
                            lines[j] = lines[j].rstrip().rstrip(',')
                            break
                    break
            cleaned_stmt = '\n'.join(lines).strip()
            cur.execute(cleaned_stmt)

        # Transform seed_data.sql for SQLite compatibility
        clean_seed = re.sub(r'NOW\(\)\s*-\s*INTERVAL\s+(\d+)\s+DAY', r"datetime('now', '-\1 days')", seed_sql)
        clean_seed = clean_seed.replace('NOW()', "datetime('now')")

        for statement in clean_seed.split(';'):
            stmt = statement.strip()
            if not stmt:
                continue
            if 'ON DUPLICATE KEY UPDATE' in stmt:
                stmt = stmt.split('ON DUPLICATE KEY UPDATE')[0].strip()
            stmt = stmt.replace('INSERT INTO', 'INSERT OR IGNORE INTO')
            cur.execute(stmt)

        conn.commit()
        conn.close()
        print(f"[SUCCESS] SQLite fallback database initialized with seed data at: {sqlite_file}")
        return True

if __name__ == '__main__':
    run_init_db()
