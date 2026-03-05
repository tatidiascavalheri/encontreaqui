import os
from sqlalchemy import create_engine, text

url = os.getenv('DATABASE_URL', 'postgresql+psycopg2://app:app@localhost:5432/encontreaqui')
engine = create_engine(url)
with engine.begin() as conn:
    sql = open('migrations/001_init.sql', 'r', encoding='utf-8').read()
    for stmt in sql.split(';'):
        if stmt.strip():
            conn.execute(text(stmt))
print('migration ok')
