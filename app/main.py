from fastapi import FastAPI, Depends, HTTPException, status  # Ensure status is imported
from sqlalchemy.orm import Session
from . import models, schemas, crud, auth
from .database import SessionLocal, engine
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timedelta

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Authentication endpoint
@app.post("/token", response_model=schemas.Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if not auth.authenticate_user(form_data.username, form_data.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials", headers={"WWW-Authenticate": "Bearer"})
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(data={"sub": form_data.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

# CRUD endpoints
@app.post("/books/", response_model=schemas.BookRead)
async def create_book(book: schemas.BookCreate, db: Session = Depends(get_db), token: str = Depends(auth.oauth2_scheme)):
    return crud.create_book(db=db, book=book)

@app.get("/books/", response_model=list[schemas.BookRead])
async def read_books(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), token: str = Depends(auth.oauth2_scheme)):
    return crud.get_books(db=db, skip=skip, limit=limit)

@app.get("/books/{book_id}", response_model=schemas.BookRead)
async def read_book(book_id: int, db: Session = Depends(get_db), token: str = Depends(auth.oauth2_scheme)):
    db_book = crud.get_book(db=db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@app.put("/books/{book_id}", response_model=schemas.BookRead)
async def update_book(book_id: int, book: schemas.BookCreate, db: Session = Depends(get_db), token: str = Depends(auth.oauth2_scheme)):
    updated_book = crud.update_book(db=db, book_id=book_id, book=book)
    if updated_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated_book

@app.delete("/books/{book_id}", response_model=schemas.BookRead)
async def delete_book(book_id: int, db: Session = Depends(get_db), token: str = Depends(auth.oauth2_scheme)):
    deleted_book = crud.delete_book(db=db, book_id=book_id)
    if deleted_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return deleted_book

from .sse import router as sse_router
app.include_router(sse_router)