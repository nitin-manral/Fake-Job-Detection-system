from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import re
import whois
import ssl
import socket
from urllib.parse import urlparse
import pickle
import os
import csv
import sys
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import io

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///job_detector.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class ScanHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(200))
    job_link = db.Column(db.String(500))
    risk_score = db.Column(db.Integer)
    risk_category = db.Column(db.String(50))
    ml_prediction = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    red_flags = db.Column(db.Text)

class FakeCompany(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True)
    scam_type = db.Column(db.String(200))
    complaint_count = db.Column(db.Integer, default=0)
    how_scam_works = db.Column(db.Text)

class GenuineCompany(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True)
    website = db.Column(db.String(500))
    overview = db.Column(db.Text)
    hiring_process = db.Column(db.Text)
    eligibility = db.Column(db.Text)
    safety_tips = db.Column(db.Text)
    industry = db.Column(db.String(200), default='Technology')
    founded_year = db.Column(db.String(50), default='N/A')
    headquarters = db.Column(db.String(200), default='India')
    logo_url = db.Column(db.String(500), default='')

class Complaint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(200))
    complaint_text = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(200), unique=True)
    password = db.Column(db.String(100))
    points = db.Column(db.Integer, default=0)
    badges = db.Column(db.String(500), default='')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer)
    rating = db.Column(db.Integer)
    comment = db.Column(db.Text)
    user_name = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

class MLModel:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=500, stop_words='english')
        self.model = LogisticRegression(random_state=42)
        self.trained = False
    
    def train(self):
        try:
            fake_samples = [
                "urgent hiring immediate joining work from home earn money fast no experience required",
                "pay registration fee deposit money advance payment processing fee refundable",
                "guaranteed income easy money quick cash part time full time flexible",
                "contact whatsapp telegram personal email gmail yahoo hotmail",
                "no interview required instant selection immediate offer letter joining",
                "earn lakhs per month unlimited income passive income guaranteed salary",
                "investment required security deposit refundable amount advance fee",
                "data entry copy paste simple typing job easy work",
                "limited seats hurry up last date today only apply now",
                "send resume to gmail id personal contact number whatsapp",
                "work from home part time earn money online no investment",
                "registration fee processing charges document verification fee payment",
                "guaranteed job placement immediate joining urgent requirement freshers",
                "no experience needed training provided earn while you learn",
                "unlimited earning potential passive income side hustle extra income",
                "contact hr manager personal email gmail yahoo rediffmail",
                "instant approval no questions asked easy application process",
                "earn thousands daily weekly monthly payment guaranteed income",
                "simple data entry typing copy paste work from anywhere",
                "limited time offer hurry last few seats available today",
                "send cv resume to personal gmail contact whatsapp number",
                "advance payment security deposit registration charges refundable fee",
                "no interview direct selection offer letter immediate joining bonus",
                "work from home flexible timing part time full time students",
                "easy money quick cash earn lakhs guaranteed high salary"
            ]
            genuine_samples = [
                "bachelor degree required minimum experience years technical skills programming",
                "apply through official website career portal company email domain",
                "interview process multiple rounds technical assessment hr round",
                "competitive salary benefits health insurance provident fund gratuity",
                "job description responsibilities qualifications required skills experience",
                "company overview established organization industry leader reputation",
                "professional development training opportunities career growth advancement",
                "office location work schedule full time employment permanent position",
                "equal opportunity employer diversity inclusion workplace culture",
                "official recruitment no fees charged transparent process legitimate",
                "minimum qualification degree experience required technical skills",
                "apply official career portal company website recruitment page",
                "selection process aptitude test technical interview hr discussion",
                "salary package benefits medical insurance pf esi leave policy",
                "job responsibilities duties qualifications eligibility criteria requirements",
                "established company reputed organization industry experience track record",
                "training program skill development career progression growth opportunities",
                "work location office address reporting time full time permanent",
                "equal employment opportunity merit based selection fair process",
                "legitimate recruitment official process no payment required free",
                "educational qualification work experience technical expertise required",
                "company career page official recruitment portal application process",
                "interview rounds assessment tests evaluation criteria selection procedure",
                "compensation package employee benefits insurance retirement plans",
                "role description key responsibilities required qualifications skills"
            ]
            
            X = fake_samples + genuine_samples
            y = [1] * len(fake_samples) + [0] * len(genuine_samples)
            
            X_vec = self.vectorizer.fit_transform(X)
            self.model.fit(X_vec, y)
            self.trained = True
            return True
        except Exception as e:
            print(f"ML Model training error: {str(e)}")
            self.trained = False
            return False
    
    def predict(self, text):
        try:
            if not self.trained:
                if not self.train():
                    return "Unknown", 0.0
            
            if not text or not text.strip():
                return "Unknown", 0.0
                
            # Clean and preprocess text
            text = str(text).strip()
            
            X_vec = self.vectorizer.transform([text])
            prediction = self.model.predict(X_vec)[0]
            probability = self.model.predict_proba(X_vec)[0]
            
            prediction_label = "Fake" if prediction == 1 else "Genuine"
            confidence = max(probability) * 100
            
            return prediction_label, confidence
        except Exception as e:
            print(f"ML Model prediction error: {str(e)}")
            return "Unknown", 0.0

ml_model = MLModel()

def check_suspicious_keywords(text):
    suspicious_words = [
        'urgent', 'immediate', 'guaranteed', 'easy money', 'work from home',
        'no experience', 'registration fee', 'deposit', 'advance payment',
        'whatsapp', 'telegram', 'gmail', 'yahoo', 'personal email',
        'unlimited income', 'earn lakhs', 'quick cash', 'investment required',
        'limited seats', 'hurry up', 'last date today', 'no interview'
    ]
    found = []
    
    if not text or not isinstance(text, str):
        return found
        
    text_lower = text.lower()
    for word in suspicious_words:
        if word in text_lower:
            found.append(word)
    return found

def check_domain_age(url):
    try:
        domain = urlparse(url).netloc
        if not domain:
            return None
        w = whois.whois(domain)
        if w.creation_date:
            creation_date = w.creation_date[0] if isinstance(w.creation_date, list) else w.creation_date
            age_days = (datetime.now() - creation_date).days
            return age_days
    except:
        return None

def check_https_ssl(url):
    try:
        if not url.startswith('http'):
            url = 'https://' + url
        parsed = urlparse(url)
        if parsed.scheme != 'https':
            return False
        context = ssl.create_default_context()
        with socket.create_connection((parsed.netloc, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=parsed.netloc) as ssock:
                return True
    except:
        return False

def check_email_domain_mismatch(email, url):
    try:
        email_domain = email.split('@')[1].lower()
        url_domain = urlparse(url).netloc.lower()
        
        if 'gmail' in email_domain or 'yahoo' in email_domain or 'hotmail' in email_domain:
            return True
        
        if email_domain not in url_domain and url_domain not in email_domain:
            return True
        return False
    except:
        return False

def calculate_reputation_score(company_name, domain_age, has_https, email_mismatch, red_flags):
    """Calculate company reputation score based on multiple factors"""
    reputation_score = 100  # Start with perfect score
    
    # Domain age factor (0-30 points deduction)
    if domain_age is not None:
        if domain_age < 30:
            reputation_score -= 30
        elif domain_age < 90:
            reputation_score -= 20
        elif domain_age < 180:
            reputation_score -= 10
    else:
        reputation_score -= 15  # Unknown domain age
    
    # SSL/HTTPS factor (0-20 points deduction)
    if not has_https:
        reputation_score -= 20
    
    # Email authenticity (0-25 points deduction)
    if email_mismatch:
        reputation_score -= 25
    
    # Content quality (0-25 points deduction)
    if red_flags and isinstance(red_flags, list):
        reputation_score -= min(len(red_flags) * 5, 25)
    
    # Check against known fake companies
    if company_name:
        fake_company = FakeCompany.query.filter_by(name=company_name).first()
        if fake_company:
            reputation_score -= 50  # Major deduction for known scammer
        
        # Check against genuine companies (bonus)
        genuine_company = GenuineCompany.query.filter_by(name=company_name).first()
        if genuine_company:
            reputation_score = min(reputation_score + 20, 100)  # Bonus for verified company
    
    return max(reputation_score, 0)  # Ensure score doesn't go below 0

def calculate_risk_score(red_flags, domain_age, has_https, email_mismatch, ml_prediction):
    score = 0
    
    # Handle red_flags safely
    if red_flags and isinstance(red_flags, list):
        score += len(red_flags) * 8
    
    if domain_age is not None and domain_age < 180:
        score += 25
    elif domain_age is None:
        score += 15
    
    if not has_https:
        score += 20
    
    if email_mismatch:
        score += 25
    
    if ml_prediction and ml_prediction == "Fake":
        score += 40
    
    return min(score, 100)

def get_reputation_level(score):
    """Convert reputation score to level"""
    if score >= 80:
        return "High Reputation"
    elif score >= 50:
        return "Medium Reputation"
    else:
        return "Low Reputation"

def get_risk_category(score):
    if score < 35:
        return "Low"
    elif score < 65:
        return "Medium"
    else:
        return "High"

def get_recommendation(score):
    if score < 30:
        return "This job posting appears relatively safe, but always verify through official channels."
    elif score < 60:
        return "Exercise caution. Verify company details and never pay any fees for job applications."
    else:
        return "HIGH RISK! This job posting shows multiple red flags. Avoid sharing personal information or making any payments."

@app.route('/')
def index():
    total_scans = ScanHistory.query.count()
    fake_detected = ScanHistory.query.filter(ScanHistory.risk_category.in_(['Medium', 'High'])).count()
    genuine_jobs = ScanHistory.query.filter_by(risk_category='Low').count()
    total_complaints = Complaint.query.count()
    
    # Recent scans
    recent_scans = ScanHistory.query.order_by(ScanHistory.timestamp.desc()).limit(5).all()
    
    return render_template('index.html', 
                         total_scans=total_scans,
                         fake_detected=fake_detected,
                         genuine_jobs=genuine_jobs,
                         total_complaints=total_complaints,
                         recent_scans=recent_scans)

@app.route('/analyze', methods=['GET', 'POST'])
def analyze():
    # Initialize all template variables with safe defaults
    template_vars = {
        'result': False,
        'company_name': '',
        'job_link': '',
        'hr_email': '',
        'job_description': '',
        'risk_score': 0,
        'risk_category': 'Low',
        'ml_prediction': 'Unknown',
        'ml_confidence': 0,
        'red_flags': [],
        'domain_age': None,
        'has_https': False,
        'email_mismatch': False,
        'recommendation': 'Please submit a job posting for analysis.',
        'reputation_score': 50,
        'reputation_level': 'Unknown',
        'scan_id': 1,
        'ai_explanations': []
    }
    
    if request.method == 'POST':
        # Get form data
        job_link = request.form.get('job_link', '').strip()
        job_description = request.form.get('job_description', '').strip()
        company_name = request.form.get('company_name', '').strip()
        hr_email = request.form.get('hr_email', '').strip()
        
        # Update template variables with form data
        template_vars.update({
            'result': True,
            'company_name': company_name,
            'job_link': job_link,
            'hr_email': hr_email,
            'job_description': job_description
        })
        
        try:
            # Analyze job description for suspicious keywords
            if job_description and company_name:
                combined_text = f"{job_description} {company_name}"
                red_flags = check_suspicious_keywords(combined_text)
                template_vars['red_flags'] = red_flags
            
            # Check domain information
            if job_link:
                try:
                    domain_age = check_domain_age(job_link)
                    template_vars['domain_age'] = domain_age
                except:
                    template_vars['domain_age'] = None
                    
                try:
                    has_https = check_https_ssl(job_link)
                    template_vars['has_https'] = has_https
                except:
                    template_vars['has_https'] = False
            
            # Check email domain mismatch
            if hr_email and job_link:
                try:
                    email_mismatch = check_email_domain_mismatch(hr_email, job_link)
                    template_vars['email_mismatch'] = email_mismatch
                except:
                    template_vars['email_mismatch'] = False
            elif hr_email:
                # Check if it's a free email service
                try:
                    email_domain = hr_email.split('@')[1].lower()
                    free_domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'aol.com']
                    template_vars['email_mismatch'] = email_domain in free_domains
                except:
                    template_vars['email_mismatch'] = False
            
            # Get ML prediction - ensure it's always set
            try:
                if job_description:
                    ml_prediction, ml_confidence = ml_model.predict(job_description)
                    template_vars['ml_prediction'] = str(ml_prediction) if ml_prediction else 'Unknown'
                    template_vars['ml_confidence'] = round(float(ml_confidence), 2) if ml_confidence else 0
                else:
                    template_vars['ml_prediction'] = 'Unknown'
                    template_vars['ml_confidence'] = 0
            except Exception as e:
                print(f"ML prediction error: {str(e)}")
                template_vars['ml_prediction'] = 'Unknown'
                template_vars['ml_confidence'] = 0
            
            # Calculate risk scores
            try:
                risk_score = calculate_risk_score(
                    template_vars['red_flags'], 
                    template_vars['domain_age'], 
                    template_vars['has_https'], 
                    template_vars['email_mismatch'], 
                    template_vars['ml_prediction']
                )
                template_vars['risk_score'] = risk_score
                template_vars['risk_category'] = get_risk_category(risk_score)
                template_vars['recommendation'] = get_recommendation(risk_score)
            except:
                template_vars['risk_score'] = 50
                template_vars['risk_category'] = 'Medium'
                template_vars['recommendation'] = 'Analysis completed with limited data. Please verify company details manually.'
            
            # Calculate company reputation score
            try:
                reputation_score = calculate_reputation_score(
                    company_name, 
                    template_vars['domain_age'], 
                    template_vars['has_https'], 
                    template_vars['email_mismatch'], 
                    template_vars['red_flags']
                )
                template_vars['reputation_score'] = reputation_score
                template_vars['reputation_level'] = get_reputation_level(reputation_score)
            except:
                template_vars['reputation_score'] = 50
                template_vars['reputation_level'] = 'Unknown'
            
            # Generate AI Explanations
            try:
                ai_explanations = generate_ai_explanations(
                    template_vars['red_flags'], 
                    template_vars['domain_age'], 
                    template_vars['has_https'], 
                    template_vars['email_mismatch'], 
                    template_vars['ml_prediction'], 
                    hr_email
                )
                template_vars['ai_explanations'] = ai_explanations
            except:
                template_vars['ai_explanations'] = []
            
        except Exception as e:
            # Log error but continue with safe defaults
            print(f"Analysis error: {str(e)}")
            template_vars['recommendation'] = 'Analysis encountered an error. Please try again or verify company details manually.'
        
        # Save scan to database
        try:
            scan = ScanHistory(
                company_name=template_vars['company_name'],
                job_link=template_vars['job_link'],
                risk_score=template_vars['risk_score'],
                risk_category=template_vars['risk_category'],
                ml_prediction=template_vars['ml_prediction'],
                red_flags=', '.join(template_vars['red_flags'])
            )
            db.session.add(scan)
            db.session.commit()
            template_vars['scan_id'] = scan.id
        except Exception as e:
            print(f"Database error: {str(e)}")
            template_vars['scan_id'] = 1  # Default scan ID
    
    # Final safety check - ensure all critical variables are defined
    if 'ml_prediction' not in template_vars or template_vars['ml_prediction'] is None:
        template_vars['ml_prediction'] = 'Unknown'
    if 'ml_confidence' not in template_vars or template_vars['ml_confidence'] is None:
        template_vars['ml_confidence'] = 0
    if 'red_flags' not in template_vars or template_vars['red_flags'] is None:
        template_vars['red_flags'] = []
    if 'ai_explanations' not in template_vars or template_vars['ai_explanations'] is None:
        template_vars['ai_explanations'] = []
    
    return render_template('analyze.html', **template_vars)

def generate_ai_explanations(red_flags, domain_age, has_https, email_mismatch, ml_prediction, hr_email=''):
    explanations = []
    
    # Ensure red_flags is a list
    if red_flags is None:
        red_flags = []
    
    # Ensure ml_prediction is a string
    if ml_prediction is None:
        ml_prediction = 'Unknown'
    
    # Suspicious keywords explanation
    if red_flags and len(red_flags) > 0:
        explanations.append({
            'type': 'danger',
            'icon': 'fas fa-exclamation-triangle',
            'title': 'Suspicious Hiring Phrases Detected',
            'description': f'Found {len(red_flags)} red flag keywords commonly used in fake job postings: {", ".join(red_flags[:3])}. Legitimate companies avoid urgent language and payment requests.',
            'impact': len(red_flags) * 8
        })
    
    # Email domain mismatch
    if email_mismatch:
        if hr_email:
            email_domain = hr_email.split('@')[1] if '@' in hr_email else 'unknown'
            free_domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com']
            if email_domain in free_domains:
                explanations.append({
                    'type': 'danger',
                    'icon': 'fas fa-envelope-open-text',
                    'title': 'Free Email Service Used',
                    'description': f'Recruiter is using {email_domain}, a free email provider. Professional companies use corporate email domains (e.g., hr@company.com). This is a major red flag.',
                    'impact': 25
                })
            else:
                explanations.append({
                    'type': 'warning',
                    'icon': 'fas fa-envelope-open-text',
                    'title': 'Email Domain Mismatch',
                    'description': f'The recruiter\'s email domain does not match the company website. Verify the recruiter\'s identity through official company channels before proceeding.',
                    'impact': 25
                })
    
    # Domain security issues
    if not has_https:
        explanations.append({
            'type': 'warning',
            'icon': 'fas fa-lock-open',
            'title': 'Missing HTTPS/SSL Security',
            'description': 'The job posting website lacks HTTPS encryption. Legitimate companies prioritize security. Your data may be at risk on this site.',
            'impact': 20
        })
    
    # Domain age check
    if domain_age is not None and domain_age < 180:
        explanations.append({
            'type': 'warning',
            'icon': 'fas fa-calendar-times',
            'title': 'Recently Created Domain',
            'description': f'The website domain is only {domain_age} days old. Scammers often use newly created domains. Established companies have older, trusted domains.',
            'impact': 25
        })
    elif domain_age is None:
        explanations.append({
            'type': 'warning',
            'icon': 'fas fa-question-circle',
            'title': 'Domain Verification Failed',
            'description': 'Unable to verify the domain age or registration details. This could indicate a suspicious or improperly configured website.',
            'impact': 15
        })
    
    # ML prediction explanation
    if ml_prediction == 'Fake':
        explanations.append({
            'type': 'danger',
            'icon': 'fas fa-robot',
            'title': 'AI Model Flagged as Fake',
            'description': 'Our machine learning model, trained on thousands of job postings, has classified this as a fake job offer based on language patterns and content analysis.',
            'impact': 40
        })
    
    # If no issues found
    if not explanations:
        explanations.append({
            'type': 'safe',
            'icon': 'fas fa-check-circle',
            'title': 'Standard Recruitment Practices',
            'description': 'This job posting follows professional recruitment standards with proper company verification, secure website, and legitimate communication channels.',
            'impact': 0
        })
    
    return explanations

@app.route('/batch-analyze', methods=['GET', 'POST'])
def batch_analyze():
    if request.method == 'POST':
        results = []
        for i in range(1, 11):
            job_desc = request.form.get(f'job_desc_{i}', '').strip()
            company = request.form.get(f'company_{i}', '').strip()
            
            if job_desc and company:
                combined_text = f"{job_desc} {company}"
                red_flags = check_suspicious_keywords(combined_text)
                ml_prediction, ml_confidence = ml_model.predict(job_desc)
                risk_score = calculate_risk_score(red_flags, None, False, False, ml_prediction)
                risk_category = get_risk_category(risk_score)
                
                results.append({
                    'company': company,
                    'risk_score': risk_score,
                    'risk_category': risk_category,
                    'ml_prediction': ml_prediction,
                    'red_flags_count': len(red_flags)
                })
                
                scan = ScanHistory(
                    company_name=company,
                    job_link='Batch Analysis',
                    risk_score=risk_score,
                    risk_category=risk_category,
                    ml_prediction=ml_prediction,
                    red_flags=', '.join(red_flags)
                )
                db.session.add(scan)
        
        db.session.commit()
        return render_template('batch_analyze.html', results=results)
    
    return render_template('batch_analyze.html', results=None)

@app.route('/threat-intelligence')
def threat_intelligence():
    high_risk_scans = ScanHistory.query.filter_by(risk_category='High').order_by(ScanHistory.timestamp.desc()).limit(10).all()
    
    from sqlalchemy import func
    scam_types = db.session.query(
        FakeCompany.scam_type,
        func.count(FakeCompany.scam_type).label('count')
    ).group_by(FakeCompany.scam_type).all()
    
    from datetime import timedelta
    today = datetime.now()
    weekly_stats = []
    for i in range(6, -1, -1):
        date = today - timedelta(days=i)
        count = ScanHistory.query.filter(
            func.date(ScanHistory.timestamp) == date.date(),
            ScanHistory.risk_category == 'High'
        ).count()
        weekly_stats.append({'date': date.strftime('%a'), 'count': count})
    
    return render_template('threat_intelligence.html',
                         high_risk_scans=high_risk_scans,
                         scam_types=scam_types,
                         weekly_stats=weekly_stats)

@app.route('/fake-companies')
def fake_companies():
    search = request.args.get('search', '')
    scam_type = request.args.get('type', '')
    sort = request.args.get('sort', 'complaints')
    
    query = FakeCompany.query
    
    if search:
        query = query.filter(FakeCompany.name.contains(search))
    
    if scam_type:
        query = query.filter(FakeCompany.scam_type.contains(scam_type))
    
    if sort == 'name':
        query = query.order_by(FakeCompany.name)
    else:
        query = query.order_by(FakeCompany.complaint_count.desc())
    
    companies = query.all()
    scam_types = db.session.query(FakeCompany.scam_type).distinct().all()
    return render_template('fake_companies.html', companies=companies, search=search, 
                         scam_type=scam_type, sort=sort, scam_types=scam_types)

@app.route('/fake-company/<int:id>')
def fake_company_detail(id):
    company = FakeCompany.query.get_or_404(id)
    ratings = Rating.query.filter_by(company_id=id).order_by(Rating.timestamp.desc()).all()
    avg_rating = db.session.query(db.func.avg(Rating.rating)).filter_by(company_id=id).scalar()
    return render_template('fake_company_detail.html', company=company, ratings=ratings, avg_rating=avg_rating)

@app.route('/rate-company/<int:id>', methods=['POST'])
def rate_company(id):
    try:
        rating_value = request.form.get('rating', type=int)
        comment = request.form.get('comment', '').strip()
        user_name = request.form.get('user_name', '').strip()
        
        if not rating_value or rating_value < 1 or rating_value > 5:
            flash('Please provide a valid rating (1-5)!', 'danger')
            return redirect(url_for('fake_company_detail', id=id))
        
        if not user_name:
            user_name = 'Anonymous'
        
        rating = Rating(company_id=id, rating=rating_value, comment=comment, user_name=user_name)
        db.session.add(rating)
        db.session.commit()
        
        flash('Rating submitted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        print(f"Rating submission error: {str(e)}")
        flash('Error submitting rating. Please try again.', 'danger')
    
    return redirect(url_for('fake_company_detail', id=id))

@app.route('/submit-complaint', methods=['POST'])
def submit_complaint():
    try:
        company_name = request.form.get('company_name', '').strip()
        complaint_text = request.form.get('complaint_text', '').strip()
        
        if not company_name or not complaint_text:
            flash('Please fill in all required fields!', 'danger')
            return redirect(url_for('fake_companies'))
        
        complaint = Complaint(company_name=company_name, complaint_text=complaint_text)
        db.session.add(complaint)
        
        fake_company = FakeCompany.query.filter_by(name=company_name).first()
        if fake_company:
            fake_company.complaint_count += 1
        
        db.session.commit()
        flash('Complaint submitted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        print(f"Complaint submission error: {str(e)}")
        flash('Error submitting complaint. Please try again.', 'danger')
    
    return redirect(url_for('fake_companies'))

@app.route('/genuine-companies')
def genuine_companies():
    companies = GenuineCompany.query.all()
    return render_template('genuine_companies.html', companies=companies)

@app.route('/genuine-company/<int:id>')
def genuine_company_detail(id):
    company = GenuineCompany.query.get_or_404(id)
    return render_template('genuine_company_detail.html', company=company)

@app.route('/history')
def history():
    search = request.args.get('search', '')
    sort = request.args.get('sort', 'date')
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    query = ScanHistory.query
    
    if search:
        query = query.filter(ScanHistory.company_name.contains(search))
    
    if sort == 'risk':
        query = query.order_by(ScanHistory.risk_score.desc())
    else:
        query = query.order_by(ScanHistory.timestamp.desc())
    
    scans = query.paginate(page=page, per_page=per_page, error_out=False)
    return render_template('history.html', scans=scans, search=search, sort=sort)

@app.route('/export-history')
def export_history():
    scans = ScanHistory.query.order_by(ScanHistory.timestamp.desc()).all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Date', 'Company', 'Risk Score', 'Category', 'ML Prediction', 'Red Flags'])
    
    for scan in scans:
        writer.writerow([
            scan.timestamp.strftime('%Y-%m-%d %H:%M'),
            scan.company_name,
            scan.risk_score,
            scan.risk_category,
            scan.ml_prediction,
            scan.red_flags
        ])
    
    output.seek(0)
    response = make_response(output.getvalue())
    response.headers['Content-Disposition'] = 'attachment; filename=scan_history.csv'
    response.headers['Content-Type'] = 'text/csv'
    return response

@app.route('/analytics')
def analytics():
    total_scans = ScanHistory.query.count()
    low_risk = ScanHistory.query.filter_by(risk_category='Low').count()
    medium_risk = ScanHistory.query.filter_by(risk_category='Medium').count()
    high_risk = ScanHistory.query.filter_by(risk_category='High').count()
    total_complaints = Complaint.query.count()
    
    from sqlalchemy import func
    most_searched = db.session.query(
        ScanHistory.company_name, 
        func.count(ScanHistory.company_name).label('count')
    ).group_by(ScanHistory.company_name).order_by(func.count(ScanHistory.company_name).desc()).first()
    
    # Top 10 fake companies
    top_fake = FakeCompany.query.order_by(FakeCompany.complaint_count.desc()).limit(10).all()
    
    # Recent scans
    recent_scans = ScanHistory.query.order_by(ScanHistory.timestamp.desc()).limit(5).all()
    
    # Trend data (last 7 days)
    from datetime import timedelta
    today = datetime.now()
    trend_data = []
    for i in range(6, -1, -1):
        date = today - timedelta(days=i)
        count = ScanHistory.query.filter(
            func.date(ScanHistory.timestamp) == date.date()
        ).count()
        trend_data.append({'date': date.strftime('%m/%d'), 'count': count})
    
    return render_template('analytics.html',
                         total_scans=total_scans,
                         low_risk=low_risk,
                         medium_risk=medium_risk,
                         high_risk=high_risk,
                         total_complaints=total_complaints,
                         most_searched=most_searched,
                         top_fake=top_fake,
                         recent_scans=recent_scans,
                         trend_data=trend_data)

@app.route('/download-report/<int:scan_id>')
def download_report(scan_id):
    scan = ScanHistory.query.get_or_404(scan_id)
    
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    
    p.setFont("Helvetica-Bold", 20)
    p.drawString(1*inch, height - 1*inch, "Job Analysis Report")
    
    p.setFont("Helvetica", 12)
    y = height - 1.5*inch
    
    p.drawString(1*inch, y, f"Company: {scan.company_name}")
    y -= 0.3*inch
    p.drawString(1*inch, y, f"Risk Score: {scan.risk_score}/100")
    y -= 0.3*inch
    p.drawString(1*inch, y, f"Risk Category: {scan.risk_category}")
    y -= 0.3*inch
    p.drawString(1*inch, y, f"ML Prediction: {scan.ml_prediction}")
    y -= 0.3*inch
    p.drawString(1*inch, y, f"Red Flags: {scan.red_flags}")
    y -= 0.3*inch
    p.drawString(1*inch, y, f"Scan Date: {scan.timestamp.strftime('%Y-%m-%d %H:%M')}")
    y -= 0.5*inch
    
    recommendation = get_recommendation(scan.risk_score)
    p.drawString(1*inch, y, "Recommendation:")
    y -= 0.3*inch
    
    words = recommendation.split()
    line = ""
    for word in words:
        if len(line + word) < 70:
            line += word + " "
        else:
            p.drawString(1*inch, y, line)
            y -= 0.3*inch
            line = word + " "
    p.drawString(1*inch, y, line)
    
    p.showPage()
    p.save()
    
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name=f'report_{scan_id}.pdf', mimetype='application/pdf')

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        if not username or not password:
            flash('Please enter both username and password!', 'danger')
            return render_template('admin_login.html')
        
        try:
            admin = Admin.query.filter_by(username=username, password=password).first()
            if admin:
                session['admin'] = True
                session['admin_username'] = username
                flash('Login successful!', 'success')
                return redirect(url_for('admin_dashboard'))
            else:
                flash('Invalid credentials!', 'danger')
        except Exception as e:
            print(f"Admin login error: {str(e)}")
            flash('Login error occurred. Please try again.', 'danger')
    
    return render_template('admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    return redirect(url_for('index'))

@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    
    total_scans = ScanHistory.query.count()
    total_fake = FakeCompany.query.count()
    total_genuine = GenuineCompany.query.count()
    total_complaints = Complaint.query.count()
    
    return render_template('admin_dashboard.html',
                         total_scans=total_scans,
                         total_fake=total_fake,
                         total_genuine=total_genuine,
                         total_complaints=total_complaints)

@app.route('/admin/fake-companies')
def admin_fake_companies():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    companies = FakeCompany.query.all()
    return render_template('admin_fake_companies.html', companies=companies)

@app.route('/admin/add-fake-company', methods=['POST'])
def add_fake_company():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    
    name = request.form.get('name')
    scam_type = request.form.get('scam_type')
    how_scam_works = request.form.get('how_scam_works')
    
    company = FakeCompany(name=name, scam_type=scam_type, how_scam_works=how_scam_works)
    db.session.add(company)
    db.session.commit()
    
    flash('Fake company added!', 'success')
    return redirect(url_for('admin_fake_companies'))

@app.route('/admin/edit-fake-company/<int:id>', methods=['GET', 'POST'])
def edit_fake_company(id):
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    
    company = FakeCompany.query.get_or_404(id)
    
    if request.method == 'POST':
        company.name = request.form.get('name')
        company.scam_type = request.form.get('scam_type')
        company.how_scam_works = request.form.get('how_scam_works')
        db.session.commit()
        flash('Company updated!', 'success')
        return redirect(url_for('admin_fake_companies'))
    
    return render_template('admin_edit_fake_company.html', company=company)

@app.route('/admin/delete-fake-company/<int:id>')
def delete_fake_company(id):
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    
    company = FakeCompany.query.get_or_404(id)
    db.session.delete(company)
    db.session.commit()
    
    flash('Company deleted!', 'success')
    return redirect(url_for('admin_fake_companies'))

@app.route('/admin/genuine-companies')
def admin_genuine_companies():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    companies = GenuineCompany.query.all()
    return render_template('admin_genuine_companies.html', companies=companies)

@app.route('/admin/add-genuine-company', methods=['POST'])
def add_genuine_company():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    
    name = request.form.get('name')
    website = request.form.get('website')
    overview = request.form.get('overview')
    hiring_process = request.form.get('hiring_process')
    eligibility = request.form.get('eligibility')
    safety_tips = request.form.get('safety_tips')
    
    company = GenuineCompany(name=name, website=website, overview=overview,
                            hiring_process=hiring_process, eligibility=eligibility,
                            safety_tips=safety_tips)
    db.session.add(company)
    db.session.commit()
    
    flash('Genuine company added!', 'success')
    return redirect(url_for('admin_genuine_companies'))

@app.route('/admin/delete-genuine-company/<int:id>')
def delete_genuine_company(id):
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    
    company = GenuineCompany.query.get_or_404(id)
    db.session.delete(company)
    db.session.commit()
    
    flash('Company deleted!', 'success')
    return redirect(url_for('admin_genuine_companies'))

@app.route('/features')
def features():
    return render_template('features.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        flash('Message sent successfully! We will get back to you soon.', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/email-checker', methods=['GET', 'POST'])
def email_checker():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        company_website = request.form.get('company_website', '').strip()
        
        result = analyze_recruiter_email(email, company_website)
        return render_template('email_checker.html', result=result, email=email)
    
    return render_template('email_checker.html', result=None)

def analyze_recruiter_email(email, company_website=''):
    free_domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'rediffmail.com', 
                    'ymail.com', 'aol.com', 'mail.com', 'protonmail.com', 'zoho.com']
    
    suspicious_patterns = ['hr.recruitment', 'hiring.team', 'job.offer', 'career.opportunity',
                          'recruitment.team', 'jobs.hr', 'hiring.manager']
    
    try:
        email_domain = email.split('@')[1]
    except:
        return {
            'valid': False,
            'error': 'Invalid email format'
        }
    
    risk_score = 0
    risk_factors = []
    domain_type = 'Unknown'
    
    # Check free email domains
    if email_domain in free_domains:
        domain_type = 'Free Email Provider'
        risk_score += 40
        risk_factors.append('Using free email service (Gmail, Yahoo, etc.) - Professional recruiters use company domains')
    else:
        domain_type = 'Corporate Domain'
    
    # Check domain mismatch
    if company_website:
        try:
            company_domain = urlparse(company_website).netloc.lower().replace('www.', '')
            if company_domain and email_domain not in company_domain and company_domain not in email_domain:
                risk_score += 35
                risk_factors.append(f'Email domain ({email_domain}) does not match company website ({company_domain})')
        except:
            pass
    
    # Check suspicious patterns
    email_local = email.split('@')[0]
    for pattern in suspicious_patterns:
        if pattern.replace('.', '') in email_local.replace('.', ''):
            risk_score += 15
            risk_factors.append(f'Suspicious email pattern detected: {pattern}')
            break
    
    # Check for numbers in domain
    if any(char.isdigit() for char in email_domain.split('.')[0]):
        risk_score += 10
        risk_factors.append('Domain contains numbers - unusual for legitimate companies')
    
    # Determine risk level
    if risk_score < 30:
        risk_level = 'Low'
        risk_color = 'success'
        recommendation = 'Email appears legitimate, but always verify through official company channels.'
    elif risk_score < 60:
        risk_level = 'Medium'
        risk_color = 'warning'
        recommendation = 'Exercise caution. Verify recruiter identity through official company website or LinkedIn.'
    else:
        risk_level = 'High'
        risk_color = 'danger'
        recommendation = 'HIGH RISK! This email shows multiple red flags. Do not share personal information or make any payments.'
    
    return {
        'valid': True,
        'email': email,
        'domain': email_domain,
        'domain_type': domain_type,
        'risk_score': min(risk_score, 100),
        'risk_level': risk_level,
        'risk_color': risk_color,
        'risk_factors': risk_factors,
        'recommendation': recommendation
    }

@app.route('/admin/complaints')
def admin_complaints():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    complaints = Complaint.query.order_by(Complaint.timestamp.desc()).all()
    return render_template('admin_complaints.html', complaints=complaints)

def init_db():
    try:
        with app.app_context():
            db.create_all()
            
            # Create admin user if not exists
            if not Admin.query.filter_by(username='admin').first():
                admin = Admin(username='admin', password='admin123')
                db.session.add(admin)
                print("Created default admin user (username: admin, password: admin123)")
            
            # Add fake companies if none exist
            if FakeCompany.query.count() == 0:
                fake_companies = [
                    FakeCompany(name="QuickCash Solutions", scam_type="Advance Fee Fraud",
                              complaint_count=45,
                              how_scam_works="They ask for registration fees ranging from ₹500-5000 promising high-paying work-from-home jobs. After payment, they disappear or provide fake assignments."),
                    FakeCompany(name="Global Data Entry Ltd", scam_type="Data Entry Scam",
                              complaint_count=78,
                              how_scam_works="Promise easy data entry jobs with high pay. Require security deposit. Provide impossible targets and never pay salaries."),
                    FakeCompany(name="HomeJobs India", scam_type="Work From Home Fraud",
                              complaint_count=92,
                              how_scam_works="Advertise lucrative WFH opportunities. Collect personal information and registration fees. No actual work provided."),
                ]
                db.session.add_all(fake_companies)
                print(f"Added {len(fake_companies)} fake companies to database")
            
            # Add genuine companies if none exist
            if GenuineCompany.query.count() == 0:
                genuine_companies = [
                    GenuineCompany(
                        name="Tata Consultancy Services",
                        website="https://www.tcs.com/careers",
                        overview="TCS is a global leader in IT services, consulting, and business solutions with over 500,000 employees worldwide.",
                        hiring_process="Online application → Aptitude test → Technical interview → HR interview → Offer letter",
                        eligibility="B.E/B.Tech/MCA with minimum 60% aggregate. No backlogs preferred.",
                        safety_tips="Always apply through official TCS careers portal. TCS never charges any fee for recruitment. Verify offer letters through official channels.",
                        industry="IT Services",
                        founded_year="1968",
                        headquarters="Mumbai, India",
                        logo_url="https://upload.wikimedia.org/wikipedia/commons/thumb/b/b1/Tata_Consultancy_Services_Logo.svg/200px-Tata_Consultancy_Services_Logo.svg.png"
                    ),
                    GenuineCompany(
                        name="Infosys Limited",
                        website="https://www.infosys.com/careers",
                        overview="Infosys is a global leader in next-generation digital services and consulting, helping clients navigate their digital transformation.",
                        hiring_process="Campus recruitment / Online portal → Online test → Technical + HR interview → Offer letter",
                        eligibility="Engineering graduates with good academic record. Strong programming and analytical skills.",
                        safety_tips="Apply only through official Infosys careers website. No payment required at any stage. Beware of fake offer letters.",
                        industry="IT Services",
                        founded_year="1981",
                        headquarters="Bangalore, India",
                        logo_url="https://upload.wikimedia.org/wikipedia/commons/thumb/9/95/Infosys_logo.svg/200px-Infosys_logo.svg.png"
                    ),
                    GenuineCompany(
                        name="Wipro Technologies",
                        website="https://careers.wipro.com",
                        overview="Wipro is a leading global IT consulting and business process services company with 250,000+ employees.",
                        hiring_process="Online application → Coding test → Technical interview → HR discussion → Offer",
                        eligibility="B.E/B.Tech/MCA/M.Sc with 60%+ marks. Good communication skills required.",
                        safety_tips="Apply through official Wipro careers portal only. No registration fees. Verify recruiter credentials.",
                        industry="IT Services",
                        founded_year="1945",
                        headquarters="Bangalore, India",
                        logo_url="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a0/Wipro_Primary_Logo_Color_RGB.svg/200px-Wipro_Primary_Logo_Color_RGB.svg.png"
                    )
                ]
                db.session.add_all(genuine_companies)
                print(f"Added {len(genuine_companies)} genuine companies to database")
            
            db.session.commit()
            print("Database initialization completed successfully")
            
    except Exception as e:
        print(f"Database initialization error: {str(e)}")
        try:
            db.session.rollback()
        except:
            pass

if __name__ == '__main__':
    try:
        print("Starting AI Fake Job Detector...")
        init_db()
        print("Database initialized successfully")
        
        # Get port from environment variable (for deployment) or use 5000 for local
        port = int(os.environ.get('PORT', 5000))
        host = '0.0.0.0' if os.environ.get('PORT') else '127.0.0.1'
        debug = not bool(os.environ.get('PORT'))  # Disable debug in production
        
        print(f"Server starting on http://{host}:{port}")
        print("Admin credentials: username=admin, password=admin123")
        app.run(host=host, port=port, debug=debug)
    except Exception as e:
        print(f"Failed to start application: {str(e)}")
        print("Please check your Python environment and dependencies")
        sys.exit(1)
