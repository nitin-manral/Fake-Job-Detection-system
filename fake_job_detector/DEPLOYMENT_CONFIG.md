# Deployment Configuration for AI Fake Job Detector

## Environment Variables Required:
- SECRET_KEY=your-secret-key-here
- DATABASE_URL=sqlite:///job_detector.db (or PostgreSQL URL for production)

## For Render.com:
1. Build Command: pip install -r requirements.txt
2. Start Command: python app.py

## For Railway:
1. Auto-detected as Flask app
2. Uses Procfile automatically

## For Heroku:
1. Uses Procfile and requirements.txt
2. Add PostgreSQL add-on for production database

## Port Configuration:
The app will automatically use PORT environment variable if available,
otherwise defaults to 5000.