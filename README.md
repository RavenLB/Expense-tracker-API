# Expense Tracker API

A RESTful API built with Flask for tracking personal expenses. This API allows users to manage their expenses, categorize them, and view expense summaries over different time periods.

## Features

- User authentication with JWT tokens
- Create, read, update, and delete expenses
- Categorize expenses (optional)
- View expense summaries (total, average, by category)
- Filter expenses by time periods (week, month, three months)
- Secure password hashing
- Token-based logout system

## Technologies Used

- Python 3.x
- Flask
- Flask-Smorest (API documentation)
- Flask-SQLAlchemy (Database ORM)
- Flask-JWT-Extended (Authentication)
- SQLite (Database)
- Marshmallow (Schema validation)
- Passlib (Password hashing)

## Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/expense-tracker-api.git
cd expense-tracker-api
```

2. Create a virtual environment and activate it
```bash
python -m venv venv
```

3. Install the dependencies
```bash
pip install -r requirements.txt
```
4. Create a `.env` file in the root directory:
```bash
JWT_SECRET_KEY=your_secret_key
```
5. Initialize the database:
```bash
python create_db.py
```

6. Run the application
```bash
python flask run
``` 
## API Endpoints

### Authentication
- `POST /register` - Register a new user
- `POST /login` - Login and receive access token
- `POST /logout` - Logout and invalidate token

### Expenses
- `GET /expense` - Get all expenses for logged-in user
- `POST /expense` - Create a new expense
- `GET /expense/<id>` - Get specific expense
- `PUT /expense/<id>` - Update specific expense
- `DELETE /expense/<id>` - Delete specific expense
- `GET /expense/summary` - Get expense summary
- `GET /expense/summary/<period>` - Get period-specific summary (week/month/three_months)

### Categories
- `GET /category` - Get all categories
- `POST /category` - Create a new category
- `GET /category/<id>` - Get specific category
- `DELETE /category/<id>` - Delete specific category

## API Usage Examples

### 1. User Registration
```bash
curl -X POST http://localhost:5000/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "secure_password123"
  }'
```
Response:
```json
{
    "message": "User created successfully."
}
```

### 2. User Login
```bash
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "secure_password123"
  }'
```
Response:
```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### 3. Creating an Expense
```bash
curl -X POST http://localhost:5000/expense \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Groceries",
    "amount": 50.99,
    "date": "18-02-2024"
  }'
```
Response:
```json
{
    "id": 1,
    "name": "Groceries",
    "amount": 50.99,
    "date": "18-02-2024",
    "category": null
}
```

### 4. Creating a Category
```bash
curl -X POST http://localhost:5000/category \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Food"
  }'
```
Response:
```json
{
    "id": 1,
    "name": "Food",
    "expenses": []
}
```

### 5. Getting Expense Summary
```bash
curl -X GET http://localhost:5000/expense/summary \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```
Response:
```json
{
    "total_amount": 150.97,
    "count": 3,
    "average": 50.32,
    "categories": {
        "Food": 80.99,
        "Transportation": 45.00,
        "Uncategorized": 24.98
    }
}
```

### 6. Getting Period Summary
```bash
curl -X GET http://localhost:5000/expense/summary/month \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```
Response:
```json
{
    "total_amount": 120.50,
    "count": 2,
    "average": 60.25,
    "categories": {
        "Food": 80.99,
        "Uncategorized": 39.51
    }
}
```

## API Response Codes

| Status Code | Description |
|------------|-------------|
| 200 | Success |
| 201 | Resource created |
| 400 | Bad request |
| 401 | Unauthorized |
| 404 | Resource not found |
| 409 | Conflict (e.g., username already exists) |
| 500 | Server error |


## Authentication

The API uses JWT tokens for authentication. After logging in, include the access token in the Authorization header:

Authorization: Bearer <your-access-token>

## Development

The API documentation will be available at:
- Swagger UI: `http://localhost:5000/swagger-ui`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.