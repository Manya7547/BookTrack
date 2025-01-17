from sqlalchemy import Column, Integer, String, Text
from .database import Base

class Book(Base):
    __tablename__ = "books"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String)
    published_date = Column(String)
    summary = Column(Text)
    genre = Column(String)
