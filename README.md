# Book Management API

This project is a **FastAPI** application that provides **CRUD** operations for managing books in an SQLite database (`books.db`). It features **JWT-based authentication** and interactive **Swagger API Documentation** for easy exploration of the endpoints.

## Endpoints

- **POST** `/login/`: Authenticate users and generate a JWT token.
- **POST** `/books/`: Add a new book to the database.
- **GET** `/books/`: Retrieve all books with pagination.
- **GET** `/books/{id}/`: Retrieve a specific book by its ID.
- **PUT** `/books/{id}/`: Update a book's details.
- **DELETE** `/books/{id}/`: Delete a book by its ID.
- **GET** `/events/`: Real-time updates using Server-Sent Events (SSE).

## Technology Stack

- **Backend**: FastAPI
- **Database**: SQLite
- **Authentication**: JWT
- **API Documentation**: Swagger UI
- **Real-Time Communication**: SSE

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/book-management-api.git
   cd book-management-api

   ```

2. Install dependencies:

   ```
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   Run the application:
   ```

3. Run the application locally using uvicorn:

   ```
   uvicorn main:app --reload
   ```

4. Access Swagger UI:
   http://127.0.0.1:8000/docs

## Deployment

### Steps to Deploy on Heroku:

1. Install Heroku CLI (if not installed):

   ```
   # macOS
   brew install heroku

   # Windows (via Powershell as administrator)
   choco install heroku-cli

   # Linux (Debian-based)
   curl https://cli-assets.heroku.com/install.sh | sh
   ```

2. Login to Heroku:

   ```
   heroku login
   ```

3. Create a new application on Heroku:

   ```
   heroku create your-app-name
   ```

4. Deploy Your Application: Push your local Git repository to Heroku:

   ```
   git push heroku master
   ```

5. Open the Application: Once the deployment is successful, you can open your app in a browser:
   ```
   heroku open
   ```
6. Access Swagger Documentation: add /docs at the end of your Heroku app's URL : https://your-app-name.herokuapp.com/docs
