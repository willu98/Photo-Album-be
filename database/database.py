import os
import sqlalchemy as _sql
import sqlalchemy.ext.declarative as _declaritive
import sqlalchemy.orm as _orm

DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URI")
engine = _sql.create_engine(DATABASE_URL)

SessionLocal = _orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = _declaritive.declarative_base()
metadata = Base.metadata
