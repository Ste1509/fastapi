from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}" \
                          f"@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# while True:
#    try:
#        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='1234',
#                                cursor_factory=RealDictCursor)
#        cur = conn.cursor()
#        print("database connection was succesfull!!")
#        break
#    except Exception as error:
#        print("connecting to database failed, Error: ", error)
#        time.sleep(2)
