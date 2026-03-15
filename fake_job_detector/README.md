# AI-Based Fake Job Offer Detection System

## MCA Level Project

A professional Flask web application that uses AI and rule-based detection to identify fake job postings and protect job seekers from scams.

## Features

### 1. Smart Job Analyzer
- Multi-input analysis (job link, description, company name, HR email)
- Rule-based detection with suspicious keyword matching
- Domain age verification using WHOIS
- HTTPS/SSL certificate validation
- Email-domain mismatch detection
- ML classification using TF-IDF + Logistic Regression
- Risk scoring (0-100) with Low/Medium/High categories
- Red flag highlighting
- AI-powered recommendations

### 2. Fake Company Database
- Searchable database of known scam companies
- Scam type classification
- Complaint tracking system
- Detailed scam methodology explanations
- User complaint submission

### 3. Genuine Company Directory
- Verified company profiles
- Official website links
- Hiring process information
- Eligibility criteria
- Safety tips for applicants

### 4. Analytics Dashboard
- Total scan statistics
- Risk distribution visualization
- Complaint analytics
- Most searched companies
- Interactive charts using Chart.js

### 5. Analysis History
- Complete scan history
- Downloadable PDF reports
- Historical risk tracking

### 6. PDF Report Generator
- Professional analysis reports
- Risk assessment details
- Recommendations
- Downloadable format

### 7. Admin Panel
- Secure login system (username: admin, password: admin123)
- Manage fake companies database
- Manage genuine companies directory
- View and monitor complaints
- System analytics

## Tech Stack

- **Backend**: Flask, SQLAlchemy
- **Database**: SQLite
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript
- **ML**: scikit-learn (TF-IDF Vectorizer, Logistic Regression)
- **Additional**: python-whois, reportlab, Chart.js

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

3. Open browser and navigate to:
```
http://127.0.0.1:5000
```

## Project Structure

```
fake_job_detector/
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── job_detector.db        # SQLite database (auto-created)
├── README.md              # Project documentation
├── templates/             # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── analyze.html
│   ├── fake_companies.html
│   ├── fake_company_detail.html
│   ├── genuine_companies.html
│   ├── genuine_company_detail.html
│   ├── history.html
│   ├── analytics.html
│   ├── admin_login.html
│   ├── admin_dashboard.html
│   ├── admin_fake_companies.html
│   ├── admin_genuine_companies.html
│   └── admin_complaints.html
└── static/
    ├── css/
    │   └── style.css      # Dark cybersecurity theme
    └── js/
        └── script.js      # Interactive features
```

## Usage

### For Users:
1. Navigate to "Analyze Job" from sidebar
2. Enter job details (description is required)
3. Submit for analysis
4. Review risk score, ML prediction, and red flags
5. Download PDF report if needed

### For Admins:
1. Click "Admin" in sidebar
2. Login with credentials (admin/admin123)
3. Manage fake/genuine companies
4. View complaints and analytics

## ML Model

The system uses a Logistic Regression classifier trained on:
- **Fake job indicators**: Urgent hiring, registration fees, personal emails, unrealistic promises
- **Genuine job indicators**: Professional requirements, official channels, transparent processes

**Features**: TF-IDF vectorization with 500 features
**Accuracy**: Trained on balanced dataset for binary classification

## Risk Scoring Algorithm

```
Risk Score = (Red Flags × 5) + Domain Age Score + HTTPS Score + Email Mismatch Score + ML Score

- Red Flags: 5 points each
- Domain Age < 180 days: 20 points
- No HTTPS: 15 points
- Email Mismatch: 20 points
- ML Prediction "Fake": 30 points

Total: 0-100 (Low: <30, Medium: 30-60, High: >60)
```

## Security Features

- Session-based admin authentication
- SQL injection prevention via SQLAlchemy ORM
- Input validation and sanitization
- Secure password handling (Note: Use hashing in production)

## Future Enhancements

- Email verification system
- Company logo verification
- Social media profile analysis
- User registration and personalized dashboards
- API integration with job portals
- Advanced NLP models (BERT, transformers)

## Credits

Developed as an MCA-level project demonstrating:
- Full-stack web development
- Machine learning integration
- Database design and management
- Security best practices
- Professional UI/UX design

## License

Educational project for academic purposes.
