from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, validates
from sqlalchemy import create_engine, Column, Integer, String, Enum, ForeignKey, Text
from enum import Enum as PyEnum

db = SQLAlchemy()
Base = declarative_base()
engine = create_engine('sqlite:///db.sqlite')
Base.metadata.create_all(engine)

class Newsletter(db.Model):
    __tablename__ = 'newsletters'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    body = db.Column(db.String)
    published_at = db.Column(db.DateTime, server_default=db.func.now())
    edited_at = db.Column(db.DateTime, onupdate=db.func.now())

class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique = True)
    phone_number = Column(String(10))

    def validate_name(self, name, key):
        if not name:
            raise ValueError('Author must have a name.')
        return name
    
    def validate_number(self, key, number):
        if number and len(number) != 10:
            raise ValueError('Phone number must be 10 digits.')
        return number
    
class Category(PyEnum):
    Fiction = 'Fiction'
    Non_Fiction = 'Non_Fiction'

class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    summary = Column(String(250))
    category = Column(Enum(Category), nullable=False)

    def validate_title(self, title, key):
        if len(title) < 250:
            raise ValueError('Title must be at least 250 characters.')
        return title
    
    def validate_content(self, content, key):
        if len(content) < 250:
            raise ValueError('Content must be at least 250 characters.')
        return content
    
    def validate_summary(self, summary, key):
        if len(summary) < 250:
            raise ValueError('Summary must be at least 250 characters.')
        return summary
    

    def __repr__(self):
        return f'<Newsletter {self.title}, published at {self.published_at}.>'
