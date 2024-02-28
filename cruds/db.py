from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from settings import DB_URL, SQL_ECHO

# DB作成
engine = create_engine(DB_URL, echo=SQL_ECHO)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
