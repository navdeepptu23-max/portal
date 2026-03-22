# Web Portal - Admin Dashboard

A modern, secure web portal built with Flask featuring user authentication, registration, profile management, and password management.

## Features

✅ **User Authentication** - Secure login system with password hashing  
✅ **User Registration** - New user signup with validation  
✅ **Dashboard** - Personal dashboard showing user info  
✅ **Profile Management** - Edit user profile and email  
✅ **Password Management** - Change password functionality  
✅ **Database Integration** - SQLite database with SQLAlchemy ORM  
✅ **Session Management** - Secure session handling  
✅ **Error Pages** - Custom 404 and 500 error pages  
✅ **Responsive UI** - Modern gradient design with responsive layouts  

## Project Structure

```
portal/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── portal.db             # SQLite database (auto-created)
└── templates/
    ├── base.html         # Base template with styling
    ├── login.html        # Login page
    ├── register.html     # Registration page
    ├── dashboard.html    # Dashboard layout
    ├── dashboard_content.html # Dashboard content
    ├── profile.html      # User profile page
    ├── change_password.html # Password change page
    ├── 404.html          # 404 error page
    └── 500.html          # 500 error page
```

## Installation

### 1. Create a Virtual Environment (Recommended)

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

## Running the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

## Usage

1. **Register** - Create a new account at `/register`
2. **Login** - Log in with your credentials
3. **Dashboard** - View your dashboard with user information
4. **Profile** - Edit your profile and email
5. **Change Password** - Update your password from the security section

## Default Features

- User registration with email and username validation
- Password hashing using Werkzeug
- SQLAlchemy ORM for database management
- Session-based authentication
- Flash messages for user feedback
- Responsive design with gradient UI

## Security Features

⚡ Password hashing with salting  
⚡ Session-based authentication  
⚡ Form validation  
⚡ SQL injection prevention (SQLAlchemy ORM)  
⚡ CSRF protection ready (can be added with Flask-WTF)  

## Database

The application uses SQLite database (`portal.db`) which is automatically created when you run the app for the first time.

### User Model

```
User
├── id (Primary Key)
├── username (Unique)
├── email (Unique)
├── password (Hashed)
├── full_name
├── created_at
└── reset_token
```

## Customization

### Change Secret Key

In `app.py`, update the `SECRET_KEY`:
```python
app.config['SECRET_KEY'] = 'your-secret-key-change-this'
```

### Change Database

To use a different database (PostgreSQL, MySQL, etc.), update:
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'your-database-url'
```

## Future Enhancements

🔄 Email verification  
🔄 Password reset via email  
🔄 Two-factor authentication  
🔄 User roles and permissions  
🔄 API endpoints  
🔄 Advanced admin dashboard  

## Troubleshooting

**Port 5000 already in use:**
```bash
python app.py --port 5001
```

**Database errors:**
Delete `portal.db` and restart the app to recreate it.

**Module not found:**
Ensure virtual environment is activated and all packages are installed.

## License

This project is open source and available for modification and distribution.

## Support

For issues and questions, please check the code or create an issue in the repository.

---

**Happy Coding!** 🚀
