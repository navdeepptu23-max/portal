# 🌐 Deployment & Domain Setup Guide

This guide covers deploying your Flask web portal to get a live domain.

## Option 1: Heroku (Easiest)

### Prerequisites
- Heroku account (sign up free at https://www.heroku.com)
- Heroku CLI installed

### Steps

1. **Install Heroku CLI**
   ```bash
   # Download from https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Login to Heroku**
   ```bash
   heroku login
   ```

3. **Create Heroku App**
   ```bash
   heroku create your-app-name
   # Example: heroku create my-web-portal
   ```

4. **Set Environment Variables**
   ```bash
   heroku config:set SECRET_KEY="your-secret-key-here"
   heroku config:set FLASK_ENV=production
   ```

5. **Deploy Your App**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git push heroku main
   ```

6. **Open Your App**
   ```bash
   heroku open
   ```

Your app will be available at: `https://your-app-name.herokuapp.com`

---

## Option 2: PythonAnywhere

### Steps

1. **Sign up** at https://www.pythonanywhere.com

2. **Upload files**
   - Go to Files tab
   - Upload your portal folder

3. **Create Web App**
   - Web tab → Add new web app
   - Choose Python 3.10+
   - Choose Flask
   - Configure path to your app

4. **Update WSGI file**
   ```python
   import sys
   path = '/home/username/portal'
   if path not in sys.path:
       sys.path.append(path)
   from app import app
   application = app
   ```

5. **Set up database**
   - Reload the web app
   - App will be live

Your domain will be: `https://username.pythonanywhere.com`

---

## Option 3: Render.com

### Steps

1. **Sign up** at https://render.com

2. **Connect GitHub**
   - Push your code to GitHub
   - Connect your GitHub account to Render

3. **Create Web Service**
   - New → Web Service
   - Select your repository
   - Name: your-app-name
   - Environment: Python 3
   - Build command: `pip install -r requirements.txt`
   - Start command: `gunicorn app:app`

4. **Deploy**
   - Render automatically deploys on push
   - Visit your app URL

Your domain will be: `https://your-app-name.onrender.com`

---

## Option 4: AWS (Advanced)

### Basic Setup
1. Create EC2 instance
2. Install Python, Flask, Gunicorn, Nginx
3. Configure SSL with Let's Encrypt
4. Point domain to instance

[See AWS documentation for detailed steps]

---

## Custom Domain Setup

### After Hosting
Once your app is live on a platform, add a custom domain:

#### For Heroku
```bash
heroku domains:add www.yourdomain.com
```

#### For Render
1. Settings tab
2. Custom Domains
3. Enter your domain
4. Update DNS records

#### For PythonAnywhere
1. Web tab
2. Add domain
3. Update DNS records

### Update DNS Records
At your domain registrar (GoDaddy, Namecheap, etc.):
- Point CNAME or A record to your hosting provider

---

## Production Checklist

Before going live:

- [ ] Change `SECRET_KEY` to a unique, secure value
- [ ] Set `DEBUG = False` in production
- [ ] Use PostgreSQL instead of SQLite (optional but recommended)
- [ ] Enable HTTPS/SSL
- [ ] Set environment variables on hosting platform
- [ ] Test login, registration, password change
- [ ] Backup database regularly
- [ ] Set up email notifications (optional)

---

## Database for Production

### Switch from SQLite to PostgreSQL

1. **Install PostgreSQL driver**
   ```bash
   pip install psycopg2-binary
   ```

2. **Update requirements.txt**
   ```
   psycopg2-binary==2.9.0
   ```

3. **Update connection string**
   ```python
   # In app.py
   app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@host:port/dbname'
   ```

---

## Environment Variables

Create a `.env` file (never commit this):
```
FLASK_ENV=production
SECRET_KEY=your-very-secure-secret-key
SQLALCHEMY_DATABASE_URI=postgresql://...
DEBUG=false
```

Load in app.py:
```python
from dotenv import load_dotenv
import os

load_dotenv()
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
```

---

## Quick Deployment Comparison

| Service | Free Tier | Custom Domain | Setup Time |
|---------|-----------|---------------|-----------|
| Heroku | Limited | Yes ($7/mo) | 5 mins |
| PythonAnywhere | Yes | Yes | 10 mins |
| Render | Yes | Yes | 10 mins |
| AWS | Limited | Yes | 30+ mins |

**Recommendation:** Start with **Render.com** or **PythonAnywhere** for free custom domain support!

---

## Troubleshooting

### 500 Error on Deployment
- Check server logs
- Verify environment variables
- Check database connection

### Database Not Found
- Run migrations: `python -c "from app import db; db.create_all()"`
- Ensure database path is correct

### Import Errors
- Check `requirements.txt` has all packages
- Restart web service after installing

---

## Next Steps

1. Choose a hosting provider
2. Get your domain name (GoDaddy, Namecheap, etc.)
3. Deploy and test
4. Configure custom domain
5. Enable HTTPS

Your portal will be live globally! 🚀
