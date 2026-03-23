import os
import secrets
import csv
import io
from functools import wraps
from datetime import datetime

from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, session, url_for, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from werkzeug.security import check_password_hash, generate_password_hash

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", secrets.token_hex(32))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///portal.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    reports = db.relationship("HospitalReport", backref="owner", lazy=True, cascade="all, delete-orphan")

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


class HospitalReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    hospital_name = db.Column(db.String(255), nullable=False)
    district = db.Column(db.String(100), nullable=False)
    month_year = db.Column(db.String(20), nullable=False)
    outpatients = db.Column(db.Integer, default=0)
    admissions = db.Column(db.Integer, default=0)
    deliveries = db.Column(db.Integer, default=0)
    deaths = db.Column(db.Integer, default=0)
    notes = db.Column(db.Text, default="")
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)


def login_required(view_func):
    @wraps(view_func)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            flash("Please login first.", "warning")
            return redirect(url_for("login"))
        user = User.query.get(session["user_id"])
        if not user or not user.is_active:
            session.pop("user_id", None)
            flash("Your account is inactive. Contact admin.", "danger")
            return redirect(url_for("login"))
        return view_func(*args, **kwargs)

    return wrapped


def admin_required(view_func):
    @wraps(view_func)
    def wrapped(*args, **kwargs):
        if "admin_id" not in session:
            flash("Admin login required.", "warning")
            return redirect(url_for("admin_login"))
        admin = User.query.get(session["admin_id"])
        if not admin or not admin.is_admin or not admin.is_active:
            session.pop("admin_id", None)
            flash("Unauthorized admin access.", "danger")
            return redirect(url_for("admin_login"))
        return view_func(*args, **kwargs)

    return wrapped


def current_user():
    user_id = session.get("user_id")
    if not user_id:
        return None
    user = User.query.get(user_id)
    if not user or not user.is_active:
        return None
    return user


def current_admin():
    admin_id = session.get("admin_id")
    if not admin_id:
        return None
    admin = User.query.get(admin_id)
    if admin and admin.is_admin and admin.is_active:
        return admin
    return None


@app.route("/")
def index():
    return render_template("index.html", user=current_user())


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not all([username, email, password]):
            flash("All fields are required.", "danger")
            return redirect(url_for("register"))

        if len(password) < 8:
            flash("Password must be at least 8 characters.", "danger")
            return redirect(url_for("register"))

        if User.query.filter_by(username=username).first():
            flash("Username already exists.", "danger")
            return redirect(url_for("register"))

        if User.query.filter_by(email=email).first():
            flash("Email already registered.", "danger")
            return redirect(url_for("register"))

        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash("Registration successful. Please login.", "success")
        return redirect(url_for("login"))

    return render_template("register.html", user=current_user())


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            if not user.is_active:
                flash("Your account is inactive. Contact admin.", "danger")
                return redirect(url_for("login"))
            session["user_id"] = user.id
            flash(f"Welcome back, {user.username}.", "success")
            return redirect(url_for("dashboard"))

        flash("Invalid username or password.", "danger")
        return redirect(url_for("login"))

    return render_template("login.html", user=current_user())


@app.route("/dashboard")
@login_required
def dashboard():
    user = current_user()
    reports = HospitalReport.query.filter_by(user_id=user.id).order_by(HospitalReport.created_at.desc()).all()
    return render_template("dashboard.html", user=user, reports=reports)


@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully.", "info")
    return redirect(url_for("index"))


@app.route("/hospital/report/new", methods=["GET", "POST"])
@login_required
def new_hospital_report():
    user = current_user()
    if request.method == "POST":
        hospital_name = request.form.get("hospital_name", "").strip()
        district = request.form.get("district", "").strip()
        month_year = request.form.get("month_year", "").strip()

        if not all([hospital_name, district, month_year]):
            flash("Hospital name, district, and month/year are required.", "danger")
            return redirect(url_for("new_hospital_report"))

        report = HospitalReport(
            user_id=user.id,
            hospital_name=hospital_name,
            district=district,
            month_year=month_year,
            outpatients=request.form.get("outpatients", 0, type=int),
            admissions=request.form.get("admissions", 0, type=int),
            deliveries=request.form.get("deliveries", 0, type=int),
            deaths=request.form.get("deaths", 0, type=int),
            notes=request.form.get("notes", "").strip(),
        )
        db.session.add(report)
        db.session.commit()

        flash("Hospital report submitted.", "success")
        return redirect(url_for("hospital_reports"))

    return render_template("hospital_report_form.html", user=user)


@app.route("/hospital/reports")
@login_required
def hospital_reports():
    user = current_user()
    reports = HospitalReport.query.filter_by(user_id=user.id).order_by(HospitalReport.created_at.desc()).all()
    return render_template("hospital_reports.html", user=user, reports=reports)


@app.route("/hospital/report/<int:report_id>")
@login_required
def hospital_report_view(report_id):
    user = current_user()
    report = HospitalReport.query.get_or_404(report_id)
    if report.user_id != user.id:
        flash("You do not have permission to view this report.", "danger")
        return redirect(url_for("hospital_reports"))
    return render_template("hospital_report_view.html", user=user, report=report)


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        admin = User.query.filter_by(username=username).first()
        if admin and admin.is_admin and admin.check_password(password):
            if not admin.is_active:
                flash("Admin account is inactive.", "danger")
                return redirect(url_for("admin_login"))
            session["admin_id"] = admin.id
            flash(f"Welcome Admin, {admin.username}.", "success")
            return redirect(url_for("admin_dashboard"))

        flash("Invalid admin credentials.", "danger")
        return redirect(url_for("admin_login"))

    return render_template("admin_login.html", user=current_user())


@app.route("/admin/dashboard")
@admin_required
def admin_dashboard():
    admin = current_admin()
    users = User.query.order_by(User.created_at.desc()).all()
    reports = HospitalReport.query.order_by(HospitalReport.created_at.desc()).all()
    stats = {
        "total_users": len(users),
        "total_reports": len(reports),
        "total_outpatients": sum(r.outpatients for r in reports),
    }
    return render_template("admin_dashboard.html", user=current_user(), admin=admin, users=users, reports=reports, stats=stats)


@app.route("/admin/users")
@admin_required
def admin_users():
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template("admin_users.html", user=current_user(), admin=current_admin(), users=users)


@app.route("/admin/users/new", methods=["GET", "POST"])
@admin_required
def admin_user_create():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        is_admin = request.form.get("is_admin") == "on"

        if not all([username, email, password]):
            flash("Username, email, and password are required.", "danger")
            return redirect(url_for("admin_user_create"))

        if len(password) < 8:
            flash("Password must be at least 8 characters.", "danger")
            return redirect(url_for("admin_user_create"))

        if User.query.filter_by(username=username).first():
            flash("Username already exists.", "danger")
            return redirect(url_for("admin_user_create"))

        if User.query.filter_by(email=email).first():
            flash("Email already exists.", "danger")
            return redirect(url_for("admin_user_create"))

        new_user = User(username=username, email=email, is_admin=is_admin, is_active=True)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash(f"Login ID created for {username}.", "success")
        return redirect(url_for("admin_users"))

    return render_template("admin_user_create.html", user=current_user(), admin=current_admin())


@app.route("/admin/users/import", methods=["GET", "POST"])
@admin_required
def admin_users_import():
    if request.method == "POST":
        csv_file = request.files.get("csv_file")
        if not csv_file or not csv_file.filename:
            flash("Please choose a CSV file.", "danger")
            return redirect(url_for("admin_users_import"))

        try:
            csv_text = csv_file.stream.read().decode("utf-8-sig")
        except Exception:
            flash("Could not read CSV file. Use UTF-8 encoding.", "danger")
            return redirect(url_for("admin_users_import"))

        reader = csv.DictReader(io.StringIO(csv_text))
        required_columns = {"username", "email", "password"}
        if not reader.fieldnames:
            flash("CSV is empty or invalid.", "danger")
            return redirect(url_for("admin_users_import"))

        headers = {h.strip().lower() for h in reader.fieldnames if h}
        missing_columns = required_columns - headers
        if missing_columns:
            missing_list = ", ".join(sorted(missing_columns))
            flash(f"Missing required CSV columns: {missing_list}", "danger")
            return redirect(url_for("admin_users_import"))

        created = 0
        skipped = 0
        batch_usernames = set()
        batch_emails = set()

        for row in reader:
            username = (row.get("username") or "").strip()
            email = (row.get("email") or "").strip().lower()
            password = row.get("password") or ""
            is_admin_raw = (row.get("is_admin") or "").strip().lower()
            is_admin = is_admin_raw in {"1", "true", "yes", "y", "on"}

            if not all([username, email, password]):
                skipped += 1
                continue

            if len(password) < 8:
                skipped += 1
                continue

            if username in batch_usernames or email in batch_emails:
                skipped += 1
                continue

            if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
                skipped += 1
                continue

            new_user = User(username=username, email=email, is_admin=is_admin, is_active=True)
            new_user.set_password(password)
            db.session.add(new_user)
            batch_usernames.add(username)
            batch_emails.add(email)
            created += 1

        db.session.commit()
        flash(f"CSV import complete. Created: {created}, Skipped: {skipped}.", "success")
        return redirect(url_for("admin_users"))

    return render_template("admin_user_import.html", user=current_user(), admin=current_admin())


@app.route("/admin/users/import/template.csv")
@admin_required
def admin_users_import_template():
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["username", "email", "password", "is_admin"])
    writer.writerow(["staff1", "staff1@example.com", "StrongPass123", "false"])
    writer.writerow(["manager1", "manager1@example.com", "StrongPass123", "true"])

    response = make_response(output.getvalue())
    response.headers["Content-Type"] = "text/csv; charset=utf-8"
    response.headers["Content-Disposition"] = "attachment; filename=users_import_template.csv"
    return response


@app.route("/admin/user/<int:user_id>/reset-password", methods=["GET", "POST"])
@admin_required
def admin_user_reset_password(user_id):
    target_user = User.query.get_or_404(user_id)

    if request.method == "POST":
        new_password = request.form.get("password", "")
        if len(new_password) < 8:
            flash("Password must be at least 8 characters.", "danger")
            return redirect(url_for("admin_user_reset_password", user_id=target_user.id))

        target_user.set_password(new_password)
        db.session.commit()
        flash(f"Password reset for {target_user.username}.", "success")
        return redirect(url_for("admin_users"))

    return render_template("admin_user_reset_password.html", user=current_user(), admin=current_admin(), target_user=target_user)


@app.route("/admin/user/<int:user_id>/toggle-active", methods=["POST"])
@admin_required
def admin_user_toggle_active(user_id):
    target_user = User.query.get_or_404(user_id)
    admin = current_admin()

    if target_user.id == admin.id and target_user.is_active:
        flash("You cannot deactivate your own account.", "danger")
        return redirect(url_for("admin_users"))

    if target_user.is_admin and target_user.is_active:
        active_admin_count = User.query.filter_by(is_admin=True, is_active=True).count()
        if active_admin_count <= 1:
            flash("Cannot deactivate the last active admin.", "danger")
            return redirect(url_for("admin_users"))

    target_user.is_active = not target_user.is_active
    db.session.commit()
    state = "activated" if target_user.is_active else "deactivated"
    flash(f"{target_user.username} has been {state}.", "info")
    return redirect(url_for("admin_users"))


@app.route("/admin/user/<int:user_id>/delete", methods=["POST"])
@admin_required
def admin_user_delete(user_id):
    target_user = User.query.get_or_404(user_id)
    admin = current_admin()

    if target_user.id == admin.id:
        flash("You cannot delete your own account.", "danger")
        return redirect(url_for("admin_users"))

    if target_user.is_admin:
        total_admin_count = User.query.filter_by(is_admin=True).count()
        if total_admin_count <= 1:
            flash("Cannot delete the last admin account.", "danger")
            return redirect(url_for("admin_users"))

    db.session.delete(target_user)
    db.session.commit()
    flash("User deleted successfully.", "info")
    return redirect(url_for("admin_users"))


@app.route("/admin/report/<int:report_id>")
@admin_required
def admin_report_view(report_id):
    report = HospitalReport.query.get_or_404(report_id)
    return render_template("admin_report_view.html", user=current_user(), admin=current_admin(), report=report)


@app.route("/admin/report/<int:report_id>/edit", methods=["GET", "POST"])
@admin_required
def admin_report_edit(report_id):
    report = HospitalReport.query.get_or_404(report_id)

    if request.method == "POST":
        report.hospital_name = request.form.get("hospital_name", "").strip()
        report.district = request.form.get("district", "").strip()
        report.month_year = request.form.get("month_year", "").strip()
        report.outpatients = request.form.get("outpatients", 0, type=int)
        report.admissions = request.form.get("admissions", 0, type=int)
        report.deliveries = request.form.get("deliveries", 0, type=int)
        report.deaths = request.form.get("deaths", 0, type=int)
        report.notes = request.form.get("notes", "").strip()

        if not all([report.hospital_name, report.district, report.month_year]):
            flash("Hospital name, district, and month/year are required.", "danger")
            return redirect(url_for("admin_report_edit", report_id=report.id))

        db.session.commit()
        flash("Report updated successfully.", "success")
        return redirect(url_for("admin_report_view", report_id=report.id))

    return render_template("admin_report_edit.html", user=current_user(), admin=current_admin(), report=report)


@app.route("/admin/report/<int:report_id>/delete", methods=["POST"])
@admin_required
def admin_report_delete(report_id):
    report = HospitalReport.query.get_or_404(report_id)
    db.session.delete(report)
    db.session.commit()
    flash("Report deleted.", "info")
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/reports/export.csv")
@admin_required
def admin_reports_export():
    reports = HospitalReport.query.order_by(HospitalReport.created_at.desc()).all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "id",
        "hospital_name",
        "district",
        "month_year",
        "owner_username",
        "owner_email",
        "outpatients",
        "admissions",
        "deliveries",
        "deaths",
        "notes",
        "created_at",
    ])

    for report in reports:
        writer.writerow([
            report.id,
            report.hospital_name,
            report.district,
            report.month_year,
            report.owner.username,
            report.owner.email,
            report.outpatients,
            report.admissions,
            report.deliveries,
            report.deaths,
            report.notes,
            report.created_at.isoformat(),
        ])

    response = make_response(output.getvalue())
    response.headers["Content-Type"] = "text/csv; charset=utf-8"
    response.headers["Content-Disposition"] = "attachment; filename=hospital_reports.csv"
    return response


@app.route("/admin/logout")
def admin_logout():
    session.pop("admin_id", None)
    flash("Admin logged out.", "info")
    return redirect(url_for("admin_login"))


def initialize_database() -> None:
    with app.app_context():
        db.create_all()

        # Lightweight migration for existing SQLite DBs created before is_active existed.
        try:
            result = db.session.execute(text("PRAGMA table_info(user)")).fetchall()
            user_columns = [row[1] for row in result]
            if "is_active" not in user_columns:
                db.session.execute(text("ALTER TABLE user ADD COLUMN is_active BOOLEAN DEFAULT 1"))
                db.session.execute(text("UPDATE user SET is_active = 1 WHERE is_active IS NULL"))
                db.session.commit()
        except Exception:
            db.session.rollback()

        admin_username = os.getenv("ADMIN_USERNAME", "admin")
        admin_email = os.getenv("ADMIN_EMAIL", "admin@nova.local")
        admin_password = os.getenv("ADMIN_PASSWORD", "Admin@123")

        admin = User.query.filter_by(username=admin_username).first()
        if not admin:
            admin = User(username=admin_username, email=admin_email, is_admin=True)
            admin.set_password(admin_password)
            db.session.add(admin)
            db.session.commit()


initialize_database()


if __name__ == "__main__":
    app.run(debug=True)
