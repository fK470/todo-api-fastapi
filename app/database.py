from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

user_name = os.getenv("MYSQL_USER")
password = os.getenv("MYSQL_ROOT_PASSWORD")
host = "db"  # docker-composeで定義したMySQLのサービス名
database_name = os.getenv("MYSQL_DATABASE")

DATABASE_URL = f'mysql+pymysql://root:{password}@{host}/{database_name}'

ENGINE = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=ENGINE)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
