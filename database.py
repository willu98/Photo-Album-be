import os
from dotenv import load_dotenv
import sqlalchemy as _sql
import sqlalchemy.ext.declarative as _declaritive
import sqlalchemy.orm as _orm

load_dotenv()
DATABASE_URL = "postgresql://%s:%s@%s:%s/%s" % (
    os.getenv('DB_USR_NAME'), 
    os.getenv('DB_PSWD'), 
    os.getenv('DB_ADDR'), 
    os.getenv('DB_PORT'),
    os.getenv('DB_NAME'))

engine = _sql.create_engine(DATABASE_URL)

SessionLocal = _orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = _declaritive.declarative_base()