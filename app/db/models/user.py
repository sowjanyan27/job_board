"""
models/user.py

This module defines the SQLAlchemy ORM model for storing user listings in the database.
It maps the 'users' table schema, ensuring structure and integrity of user data
when performing database operations.

SQLAlchemy's ORM allows easy interaction with relational databases using Python classes.
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    role = Column(String, index=True, nullable=False)