import datetime as dt
from enum import unique
import sqlalchemy as sql

import database.database as database

class User_Photos(database.Base):
    __tablename__ = "user_photos"
    id = sql.Column(sql.Integer, autoincrement=True, primary_key=True, index=True)
    username = sql.Column(sql.String)
    file_url = sql.Column(sql.String)
    user_filename = sql.Column(sql.String)
    date_created = sql.Column(sql.DateTime, default=dt.datetime.utcnow)
    
class User(database.Base):
    __tablename__ = "users"
    id = sql.Column(sql.Integer, autoincrement=True, primary_key=True, index=True)
    name = sql.Column(sql.String, index=True)
    date_created = sql.Column(sql.DateTime, default=dt.datetime.utcnow)
    username = sql.Column(sql.String, unique=True)
    password = sql.Column(sql.String, unique=True)