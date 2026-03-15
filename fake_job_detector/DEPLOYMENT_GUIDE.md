# 🚀 Free Deployment Guide - AI Fake Job Detector

## Option 1: Render.com (RECOMMENDED - Easiest)

### Steps:
1. **Create GitHub Repository**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/fake-job-detector.git
   git push -u origin main
   ```

2. **Deploy on Render**
   - Go to [render.com](https://render.com) and sign up
   - Click "New" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `python app.py`
     - **Environment**: Python 3

3. **Set Environment Variables** (Optional):
   - `SECRET_KEY`: Generate a secure key
   - `DATABASE_URL`: Will use SQLite by default

### ✅ Pros:
- Completely free (750 hours/month)
- Auto-deploys from GitHub
- Built-in SSL certificate
- Easy setup

---

## Option 2: Railway

### Steps:
1. **Push to GitHub** (same as above)
2. **Deploy on Railway**
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub
   - Click "Deploy from GitHub repo"
   - Select your repository
   - Railway auto-detects Flask app

### ✅ Pros:
- $5 free credits monthly
- Very fast deployment
- Good performance

---

## Option 3: Heroku

### Steps:
1. **Install Heroku CLI**
2. **Deploy Commands**:
   ```bash
   heroku login
   heroku create your-app-name
   git push heroku main
   ```

### ✅ Pros:
- 550 free hours/month
- Many add-ons available
- Well-documented

---

## Option 4: PythonAnywhere

### Steps:
1. **Upload Files**
   - Sign up at [pythonanywhere.com](https://pythonanywhere.com)
   - Upload your project files
   - Configure web app in dashboard

### ✅ Pros:
- Simple file upload
- Good for beginners
- Free tier available

---

## 📋 Pre-Deployment Checklist

- [x] Procfile created
- [x] runtime.txt created  
- [x] requirements.txt updated
- [x] App configured for deployment
- [ ] Push code to GitHub
- [ ] Choose deployment platform
- [ ] Deploy and test

## 🔧 Local Testing Before Deployment

```bash
# Test locally first
python app.py
# Visit http://localhost:5000
```

## 🌐 After Deployment

1. **Test all features**:
   - Job analysis
   - Admin panel (admin/admin123)
   - Database functionality

2. **Update admin credentials** for security

3. **Monitor performance** and logs

## 💡 Tips for Free Deployment

- **Render.com** is the easiest for beginners
- **Railway** offers good performance
- **Heroku** has the most documentation
- Keep your app active to avoid sleeping (free tiers)

## 🔒 Security Notes

- Change default admin password after deployment
- Use environment variables for sensitive data
- Enable HTTPS (most platforms provide this automatically)

---

**Need help?** The deployment files are ready. Just push to GitHub and follow the platform-specific steps above!