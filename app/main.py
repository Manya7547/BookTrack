# app/main.py
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from . import models, crud, schemas, auth, database, sse

app = FastAPI()

# Dependency for accessing DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# JWT Authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Route for login (JWT token generation)
@app.post("/login", response_model=schemas.Token)
def login_for_access_token(form_data: schemas.Login, db: Session = Depends(get_db)):
    user = {"username": form_data.username, "password": form_data.password}  # Add user validation
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = auth.create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}

# Secure CRUD operations
@app.post("/books/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    if not auth.verify_token(token):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token")
    return crud.create_book(db=db, book=book)

@app.get("/books/", response_model=list[schemas.Book])
def get_books(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    if not auth.verify_token(token):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token")
    return crud.get_books(db=db, skip=skip, limit=limit)

@app.get("/books/{book_id}", response_model=schemas.Book)
def get_book(book_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    if not auth.verify_token(token):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token")
    db_book = crud.get_book_by_id(db=db, book_id=book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@app.put("/books/{book_id}", response_model=schemas.Book)
def update_book(book_id: int, book: schemas.BookCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    if not auth.verify_token(token):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token")
    return crud.update_book(db=db, book_id=book_id, book=book)

@app.delete("/books/{book_id}", response_model=schemas.Book)
def delete_book(book_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    if not auth.verify_token(token):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token")
    return crud.delete_book(db=db, book_id=book_id)

# SSE Route for real-time updates
@app.get("/events")
def get_events():
    return sse.stream()




