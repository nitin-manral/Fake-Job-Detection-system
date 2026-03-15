# Threat Intelligence Quick Start Guide

## What is Threat Intelligence?

The Threat Intelligence feature automatically identifies, tracks, and analyzes malicious patterns in fake job postings to protect users from scams.

## Quick Setup (3 Steps)

### Step 1: Start the Application
```bash
python app.py
```

### Step 2: Load Sample Threats (Optional)
```bash
python init_threats.py
```

### Step 3: Access Dashboard
Open browser: `http://127.0.0.1:5000/threat-intelligence`

## Key Features at a Glance

### 🛡️ Automatic Threat Detection
- Every job scan automatically extracts threat indicators
- Suspicious emails, domains, and keywords are tracked
- Database builds over time with real usage

### 📊 Real-Time Dashboard
- **Weekly Threats**: High-risk detections in last 7 days
- **Active Scams**: Current scam types in circulation
- **Trend Chart**: 30-day threat visualization
- **Critical Indicators**: Most dangerous threats

### 🔍 Threat Indicators Tracked

| Type | Example | Risk Level |
|------|---------|------------|
| Email | hr@gmail.com | High |
| Domain | quickcash-jobs.xyz | Critical |
| Keywords | "urgent, registration fee" | High |

### 📡 API Access
```bash
curl http://localhost:5000/api/threat-feed
```

Returns JSON with latest 50 threat indicators.

## How It Works

```
Job Submission → Risk Analysis → High Risk Detected
                                        ↓
                            Extract Threat Indicators
                                        ↓
                            Store in Database
                                        ↓
                            Update Dashboard
```

## Example Workflow

1. **User submits suspicious job**
   - Job description: "Urgent hiring! Pay ₹500 registration fee..."
   - HR Email: quickjobs@gmail.com
   - Website: quickcash-jobs.xyz

2. **System analyzes and detects high risk**
   - Risk Score: 85/100
   - Category: High

3. **Threat indicators extracted**
   - Email: quickjobs@gmail.com (High)
   - Domain: quickcash-jobs.xyz (Critical)
   - Keywords: "urgent, registration fee" (High)

4. **Dashboard updates**
   - Weekly threats: +1
   - New indicators added to database
   - Trend chart updated

## Understanding Threat Levels

- **Critical** 🔴: Confirmed scam, immediate action required
- **High** 🟠: Strong indicators of fraud
- **Medium** 🟡: Suspicious patterns, investigate
- **Low** 🟢: Minor red flags, monitor

## Best Practices

### For Users
✅ Check threat dashboard before applying to jobs
✅ Verify if company email/domain is flagged
✅ Report suspicious jobs to build database

### For Administrators
✅ Monitor critical indicators weekly
✅ Review high-hit-count threats
✅ Export threat feed for external tools
✅ Analyze trends for proactive protection

## Common Questions

**Q: How are threats detected?**
A: Automatically during job analysis. High/Medium risk jobs trigger indicator extraction.

**Q: Can I add custom threats?**
A: Currently automatic. Manual addition feature coming soon.

**Q: Is the API free?**
A: Yes, for educational/personal use. Rate limiting recommended for production.

**Q: How accurate is threat detection?**
A: Improves with usage. More scans = better threat database.

## Troubleshooting

### No threats showing?
```bash
python init_threats.py  # Load sample data
```

### API not responding?
- Check Flask server is running
- Verify URL: http://localhost:5000/api/threat-feed

### Chart not displaying?
- Check internet connection (Chart.js CDN)
- Clear browser cache

## Next Steps

1. ✅ Analyze some job postings to generate real threats
2. ✅ Monitor dashboard for emerging patterns
3. ✅ Integrate threat feed with external tools
4. ✅ Share findings with community

## Need Help?

- 📖 Full documentation: `THREAT_INTELLIGENCE.md`
- 📋 Project README: `README.md`
- 🐛 Check application logs for errors

---

**Remember**: The more you use the system, the smarter it becomes! 🚀
