import psycopg2
from psycopg2.extras import RealDictCursor
from config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD, DB_PORT

def get_conn():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )

def init_db():
    conn = get_conn()
    cursor = conn.cursor()
    
    # Create applications table if not exists
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS applications (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(100) NOT NULL,
        phone VARCHAR(20) NOT NULL,
        cv_url TEXT NOT NULL,
        cv_data JSONB NOT NULL,
        status VARCHAR(10) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    conn.commit()
    cursor.close()
    conn.close()

def insert_application(name, email, phone, cv_url, cv_data, status):
    conn = get_conn()
    cursor = conn.cursor()
    
    cursor.execute(
        '''
        INSERT INTO applications (name, email, phone, cv_url, cv_data, status)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id
        ''',
        (name, email, phone, cv_url, cv_data, status)
    )
    
    application_id = cursor.fetchone()[0]
    
    conn.commit()
    cursor.close()
    conn.close()
    
    return application_id

def get_application_by_id(application_id):
    conn = get_conn()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    cursor.execute(
        '''
        SELECT * FROM applications
        WHERE id = %s
        ''',
        (application_id,)
    )
    
    application = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    return application