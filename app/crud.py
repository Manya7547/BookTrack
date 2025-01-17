from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime

def create_book(db: Session, book: schemas.BookCreate):
    if book.published_date:
        try:
            if isinstance(book.published_date, datetime):
                book.published_date = book.published_date.strftime('%Y-%m-%d')
            datetime.strptime(book.published_date, '%Y-%m-%d')  # Validate the format
        except ValueError:
            raise ValueError("Published date must be in 'YYYY-MM-DD' format.")
    
    db_book = models.Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def get_books(db: Session, skip: int = 0, limit: int = 10):
    books = db.query(models.Book).offset(skip).limit(limit).all()
    for book in books:
        if book.published_date:
            try:
                # Handle if published_date is a datetime.date object
                if isinstance(book.published_date, datetime):
                    book.published_date = book.published_date.strftime('%Y-%m-%d')
                datetime.strptime(book.published_date, '%Y-%m-%d')  # Validate format
            except ValueError:
                raise ValueError(f"Invalid date format found for book ID {book.id}")
    return books

def get_book(db: Session, book_id: int):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book:
        if db_book.published_date:
            try:
                if isinstance(db_book.published_date, datetime):
                    db_book.published_date = db_book.published_date.strftime('%Y-%m-%d')
                datetime.strptime(db_book.published_date, '%Y-%m-%d')  # Validate format
            except ValueError:
                raise ValueError(f"Invalid date format for book ID {book_id}")
        return db_book
    return None

def update_book(db: Session, book_id: int, book: schemas.BookCreate):
    db_book = get_book(db, book_id)
    if db_book:
        if book.published_date:
            try:
                if isinstance(book.published_date, datetime):
                    book.published_date = book.published_date.strftime('%Y-%m-%d')
                datetime.strptime(book.published_date, '%Y-%m-%d')  # Validate format
            except ValueError:
                raise ValueError("Published date must be in 'YYYY-MM-DD' format.")
        
        for var, value in vars(book).items():
            if value is not None:
                setattr(db_book, var, value)
        
        db.commit()
        db.refresh(db_book)
        return db_book
    return None

def delete_book(db: Session, book_id: int):
    db_book = get_book(db, book_id)
    if db_book:
        db.delete(db_book)
        db.commit()
        return db_book
    return None
