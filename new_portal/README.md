# New Portal (Flask)

A clean starter web portal with:
- Registration and login
- Session authentication
- Protected dashboard
- Hospital report submission and listing
- Admin login and reports overview
- SQLite database via SQLAlchemy

## Run locally

1. Create and activate virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Optional: create a `.env` file from `.env.example` and set `SECRET_KEY`.

4. Start app:

```powershell
python app.py
```

5. Open:
- http://127.0.0.1:5000

## Routes
- `/` home
- `/register` user registration
- `/login` user login
- `/dashboard` protected page
- `/hospital/report/new` create hospital report
- `/hospital/reports` list own reports
- `/admin/login` admin login
- `/admin/dashboard` admin panel
- `/admin/users` list portal users
- `/admin/users/new` create new login IDs
- `/admin/users/import` bulk create login IDs from CSV
- `/admin/users/import/template.csv` download CSV template
- `/admin/user/<id>/reset-password` reset user password
- `/admin/user/<id>/toggle-active` activate/deactivate account
- `/admin/user/<id>/delete` delete user account
- `/admin/report/<id>` admin report detail
- `/admin/report/<id>/edit` admin edit report
- `/admin/report/<id>/delete` admin delete report
- `/admin/reports/export.csv` download all reports as CSV
- `/logout` logout

## Default admin (change in production)
- Username: `admin`
- Password: `Admin@123`

You can override defaults with environment variables:
- `ADMIN_USERNAME`
- `ADMIN_EMAIL`
- `ADMIN_PASSWORD`

## CSV import format
Required columns:
- `username`
- `email`
- `password`

Optional columns:
- `is_admin` (`true`/`false`, `1`/`0`, `yes`/`no`)
