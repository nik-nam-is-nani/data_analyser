# Expense Tracker Flask Backend

A Python Flask backend application that connects to Aiven PostgreSQL database with user authentication and weekly expense analyzer functionality.

## Features

### User Authentication
- **POST /api/signup** - Register a new user
- **POST /api/login** - Authenticate user login
- Password hashing with Werkzeug security
- Input validation and error handling

### Weekly Expense Analyzer
- **POST /api/add_expense** - Add a new expense record
- **GET /api/get_expenses/<username>** - Get all expenses for a user
- **GET /api/weekly_summary/<username>** - Get weekly expense summary by category
- **PUT /api/expenses/<expense_id>** - Update an expense record
- **DELETE /api/expenses/<expense_id>** - Delete an expense record

### Database Models
- **Users Table**: id, username, password (hashed), created_at
- **Expenses Table**: id, username, category, amount, week_date, created_at

## Setup Instructions

### Prerequisites
- Python 3.11+
- PostgreSQL database (Aiven)
- Virtual environment

### Installation

1. **Navigate to the project directory:**
   ```bash
   cd expense_tracker_backend
   ```

2. **Activate the virtual environment:**
   ```bash
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure database connection:**
   The application is pre-configured to connect to your Aiven PostgreSQL database:
   - Host: pg-7fabea4-nikshithkyathrigi2005-3753.g.aivencloud.com
   - Port: 14586
   - Database: defaultdb
   - User: avnadmin
   - SSL mode: require

5. **Run the application:**
   ```bash
   python src/main.py
   ```

   The server will start on `http://0.0.0.0:5003`

## API Documentation

### Authentication Endpoints

#### POST /api/signup
Register a new user account.

**Request Body:**
```json
{
  "username": "your_username",
  "password": "your_password"
}
```

**Response (Success - 201):**
```json
{
  "message": "User created successfully",
  "user": {
    "id": 1,
    "username": "your_username",
    "created_at": "2024-08-19T04:00:00"
  }
}
```

**Response (Error - 409):**
```json
{
  "error": "Username already exists"
}
```

#### POST /api/login
Authenticate user login.

**Request Body:**
```json
{
  "username": "your_username",
  "password": "your_password"
}
```

**Response (Success - 200):**
```json
{
  "message": "Login successful",
  "user": {
    "id": 1,
    "username": "your_username",
    "created_at": "2024-08-19T04:00:00"
  }
}
```

**Response (Error - 401):**
```json
{
  "error": "Invalid username or password"
}
```

### Expense Management Endpoints

#### POST /api/add_expense
Add a new expense record.

**Request Body:**
```json
{
  "username": "your_username",
  "category": "Food",
  "amount": 25.50,
  "week_date": "2024-08-19"
}
```

**Response (Success - 201):**
```json
{
  "message": "Expense added successfully",
  "expense": {
    "id": 1,
    "username": "your_username",
    "category": "Food",
    "amount": 25.50,
    "week_date": "2024-08-19",
    "created_at": "2024-08-19T04:00:00"
  }
}
```

#### GET /api/get_expenses/<username>
Get all expenses for a specific user.

**Response (Success - 200):**
```json
{
  "username": "your_username",
  "expenses": [
    {
      "id": 1,
      "username": "your_username",
      "category": "Food",
      "amount": 25.50,
      "week_date": "2024-08-19",
      "created_at": "2024-08-19T04:00:00"
    }
  ],
  "total_expenses": 1
}
```

#### GET /api/weekly_summary/<username>
Get weekly expense summary grouped by category for the last week.

**Response (Success - 200):**
```json
{
  "username": "your_username",
  "period": "2024-08-12 to 2024-08-19",
  "category_summary": {
    "Food": 125.75,
    "Travel": 45.00,
    "Utilities": 200.00
  },
  "total_amount": 370.75,
  "highest_category": {
    "category": "Utilities",
    "amount": 200.00
  },
  "expense_count": 8
}
```

#### PUT /api/expenses/<expense_id>
Update an existing expense record.

**Request Body:**
```json
{
  "category": "Updated Category",
  "amount": 30.00,
  "week_date": "2024-08-20"
}
```

#### DELETE /api/expenses/<expense_id>
Delete an expense record.

**Response (Success - 200):**
```json
{
  "message": "Expense deleted successfully"
}
```

## Testing the API

You can test the API endpoints using curl commands:

### Test Signup
```bash
curl -X POST http://localhost:5003/api/signup \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass123"}'
```

### Test Login
```bash
curl -X POST http://localhost:5003/api/login \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass123"}'
```

### Test Add Expense
```bash
curl -X POST http://localhost:5003/api/add_expense \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "category": "Food", "amount": 25.50, "week_date": "2024-08-19"}'
```

### Test Get Expenses
```bash
curl -X GET http://localhost:5003/api/get_expenses/testuser
```

### Test Weekly Summary
```bash
curl -X GET http://localhost:5003/api/weekly_summary/testuser
```

## Frontend Integration

The Flask application serves static files from the `src/static/` directory. Your HTML files have been copied there:
- `login.html` - User login page
- `signup.html` - User registration page
- `mainpage.html` - Main dashboard
- `week.html` - Weekly expense analyzer

To integrate with the frontend, update the JavaScript in your HTML files to make API calls to the Flask endpoints:

```javascript
// Example: Signup functionality
function handleSignup(event) {
    event.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    fetch('/api/signup', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            alert('Signup successful!');
            // Redirect to login or main page
        } else {
            alert('Error: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Network error occurred');
    });
}
```

## Database Schema

The application automatically creates the following tables:

### users
- `id` (Primary Key, Integer)
- `username` (String, Unique, Not Null)
- `password` (String, Not Null, Hashed)
- `created_at` (DateTime, Default: Current Time)

### expenses
- `id` (Primary Key, Integer)
- `username` (Foreign Key to users.username, String, Not Null)
- `category` (String, Not Null)
- `amount` (Numeric(10,2), Not Null)
- `week_date` (Date, Not Null)
- `created_at` (DateTime, Default: Current Time)

## Error Handling

The API includes comprehensive error handling:
- Input validation for all endpoints
- Database error handling with rollback
- Proper HTTP status codes
- Descriptive error messages

## Security Features

- Password hashing using Werkzeug's security functions
- Input validation and sanitization
- CORS enabled for frontend integration
- SQL injection protection through SQLAlchemy ORM

## Deployment

For production deployment:
1. Update `requirements.txt` with all dependencies
2. Configure environment variables for database credentials
3. Use a production WSGI server like Gunicorn
4. Set up proper SSL/TLS certificates
5. Configure firewall and security groups

## Troubleshooting

If you encounter issues:
1. Check that the virtual environment is activated
2. Verify database connection credentials
3. Ensure all dependencies are installed
4. Check that the database server is accessible
5. Review the Flask application logs for errors

## File Structure

```
expense_tracker_backend/
├── venv/                    # Virtual environment
├── src/
│   ├── models/
│   │   └── user.py         # Database models
│   ├── routes/
│   │   ├── user.py         # Authentication routes
│   │   └── expense.py      # Expense management routes
│   ├── static/             # Frontend files
│   │   ├── login.html
│   │   ├── signup.html
│   │   ├── mainpage.html
│   │   └── week.html
│   └── main.py             # Main Flask application
├── requirements.txt        # Python dependencies
├── README.md              # This documentation
└── test_db.py             # Database connection test
```

This Flask backend provides a complete solution for user authentication and expense management with PostgreSQL integration.

