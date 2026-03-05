import os
from sqlalchemy import create_engine, text

url = os.getenv('DATABASE_URL', 'postgresql+psycopg2://app:app@localhost:5432/encontreaqui')
engine = create_engine(url)

with engine.begin() as conn:
    conn.execute(text("INSERT INTO categories (name) VALUES ('Eletricista') ON CONFLICT DO NOTHING"))
    for i in range(1,6):
        conn.execute(text(f"INSERT INTO users (id, role, email, password_hash, is_verified) VALUES ({i}, 'professional', 'pro{i}@mail.com', 'x', true) ON CONFLICT DO NOTHING"))
        conn.execute(text(f"INSERT INTO professionals (id, user_id, description, price_cents, location, city, uf) VALUES ({i},{i},'Pro {i}',10000,ST_GeogFromText('POINT({-46.66 + i*0.01} {-23.56 + i*0.01})'),'São Paulo','SP') ON CONFLICT DO NOTHING"))
        conn.execute(text(f"INSERT INTO professional_categories (professional_id, category_id) VALUES ({i},1) ON CONFLICT DO NOTHING"))
print('seed ok')
