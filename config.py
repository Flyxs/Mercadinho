import os

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://mercadinho_user:mercadinho_pass@localhost:5432/mercadinho_db')
