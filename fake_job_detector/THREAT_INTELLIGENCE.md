# Threat Intelligence Feature Documentation

## Overview
The Threat Intelligence Dashboard provides real-time monitoring and analysis of job scam threats, helping identify patterns and protect users from emerging fraud schemes.

## Key Features

### 1. Automated Threat Indicator Extraction
- **Email Indicators**: Automatically flags suspicious email addresses (Gmail, Yahoo, Hotmail used for recruitment)
- **Domain Indicators**: Tracks malicious domains associated with fake job postings
- **Keyword Indicators**: Identifies high-risk keyword combinations in job descriptions
- **Auto-Learning**: System learns from each scan and builds threat database

### 2. Threat Intelligence Dashboard
Access via: `/threat-intelligence`

**Metrics Displayed:**
- Weekly high-risk threat count (last 7 days)
- Active scam types
- Recent threat detections
- Critical threat indicators

**Visualizations:**
- 30-day threat trend chart
- Trending scam type distribution
- Recent high-risk detections timeline

### 3. Threat Indicator Database
**Indicator Types:**
- `email`: Suspicious email addresses
- `domain`: Malicious domains
- `keyword`: High-risk keyword patterns
- `ip`: Suspicious IP addresses (future)

**Threat Levels:**
- `Critical`: Confirmed scam indicators with high confidence
- `High`: Strong indicators of fraudulent activity
- `Medium`: Suspicious patterns requiring investigation
- `Low`: Minor red flags

**Tracking Metrics:**
- First seen timestamp
- Last seen timestamp
- Hit count (number of times detected)
- Description of threat

### 4. API Endpoint
**Threat Feed API**: `/api/threat-feed`

Returns JSON array of latest 50 threat indicators:
```json
[
  {
    "type": "email",
    "value": "scam@gmail.com",
    "level": "Critical",
    "hits": 45,
    "last_seen": "2024-01-15 10:30"
  }
]
```

**Use Cases:**
- Integration with external security tools
- Automated threat blocking
- Real-time alert systems
- Threat intelligence sharing

## How It Works

### Automatic Threat Detection Flow
1. User submits job posting for analysis
2. System analyzes and calculates risk score
3. If risk is Medium/High:
   - Extract threat indicators (emails, domains, keywords)
   - Check if indicator exists in database
   - If exists: Increment hit count, update last_seen
   - If new: Create new threat indicator entry
4. Threat dashboard updates in real-time

### Threat Scoring Algorithm
```
Indicator Threat Level = f(hit_count, recency, pattern_match)

Critical: hit_count >= 50 OR confirmed_scam
High: hit_count >= 20 OR multiple_reports
Medium: hit_count >= 5 OR suspicious_pattern
Low: hit_count < 5
```

## Usage Guide

### For Users
1. Navigate to "Threat Intelligence" from sidebar
2. View current threat landscape
3. Check if specific indicators are flagged
4. Stay informed about trending scams

### For Administrators
1. Monitor threat dashboard regularly
2. Review critical indicators
3. Export threat feed for external systems
4. Analyze trends for proactive protection

### For Developers
**Integrate Threat Feed:**
```python
import requests

response = requests.get('http://localhost:5000/api/threat-feed')
threats = response.json()

for threat in threats:
    if threat['level'] == 'Critical':
        block_indicator(threat['value'])
```

## Database Schema

### ThreatIndicator Model
```python
class ThreatIndicator(db.Model):
    id = Integer (Primary Key)
    indicator_type = String(50)      # email, domain, keyword, ip
    indicator_value = String(500)    # Actual indicator value
    threat_level = String(20)        # Critical, High, Medium, Low
    description = Text               # Threat description
    first_seen = DateTime            # First detection timestamp
    last_seen = DateTime             # Latest detection timestamp
    hit_count = Integer              # Number of detections
```

## Setup Instructions

### 1. Initialize Database
The threat indicator table is automatically created when you run the app:
```bash
python app.py
```

### 2. Load Sample Data (Optional)
```bash
python init_threats.py
```

### 3. Access Dashboard
Navigate to: `http://127.0.0.1:5000/threat-intelligence`

## Advanced Features

### Threat Trend Analysis
- 30-day historical trend visualization
- Pattern recognition for emerging threats
- Predictive analytics (future enhancement)

### Community Intelligence
- Crowdsourced threat reporting
- Collaborative threat database
- Real-time threat sharing

### Integration Capabilities
- REST API for threat feed
- Webhook support (future)
- SIEM integration (future)
- Threat intelligence platform integration (future)

## Security Considerations

1. **Data Privacy**: Threat indicators are anonymized and aggregated
2. **False Positives**: Manual review recommended for critical actions
3. **Rate Limiting**: API endpoints should be rate-limited in production
4. **Access Control**: Threat feed API should require authentication in production

## Future Enhancements

1. **Machine Learning**: Automated threat classification
2. **Geolocation**: Track threat origins by location
3. **Reputation Scoring**: Company reputation based on threat indicators
4. **Alert System**: Real-time notifications for critical threats
5. **Threat Hunting**: Proactive threat discovery tools
6. **Integration**: Connect with external threat intelligence feeds
7. **Blockchain**: Immutable threat indicator ledger
8. **AI Analysis**: Natural language processing for threat descriptions

## Troubleshooting

### No Threats Showing
- Run `python init_threats.py` to load sample data
- Analyze some high-risk job postings to generate indicators

### API Not Working
- Check Flask server is running
- Verify route: `/api/threat-feed`
- Check database connection

### Chart Not Displaying
- Ensure Chart.js CDN is accessible
- Check browser console for JavaScript errors
- Verify threat_trend data is being passed to template

## Support

For issues or questions:
- Check application logs
- Review database entries
- Verify all dependencies are installed
- Ensure database migrations are complete

## Credits

Threat Intelligence feature developed as part of the AI-Based Fake Job Offer Detection System - MCA Level Project.
