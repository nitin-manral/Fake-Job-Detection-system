# 🚀 QUICK START GUIDE

## Method 1: Double Click (Easiest)
1. Double-click `START.bat`
2. Wait for server to start
3. Open browser: http://localhost:5000

## Method 2: Command Line
```bash
cd "c:\Users\LENOVO\OneDrive\Desktop\SEM 2 PROJECT MCA\fake_job_detector"
python app.py
```

## Method 3: If Python Not Working
```bash
py app.py
```

---

## 🔧 If Errors Occur:

### Error: "Python not found"
**Fix:** Install Python from python.org

### Error: "Module not found"
**Fix:** 
```bash
pip install Flask Flask-SQLAlchemy scikit-learn python-whois reportlab
```

### Error: "Port already in use"
**Fix:** Press Ctrl+C and run again

### Error: "Database locked"
**Fix:** Delete `instance` folder and run again

---

## 📱 Access URLs:

- **Local:** http://localhost:5000
- **Same WiFi:** http://YOUR_IP:5000

---

## 🔐 Login Credentials:

**Admin Panel:**
- Username: `admin`
- Password: `admin123`

---

## ✅ Features to Test:

1. **Home** - View statistics
2. **Analyze Job** - Test with fake job description
3. **Batch Analysis** - Analyze multiple jobs
4. **Threat Intelligence** - View scam trends
5. **Fake Companies** - Search database
6. **Genuine Companies** - View 10 companies
7. **History** - See past scans
8. **Analytics** - View charts
9. **Admin** - Manage data

---

## 🎯 Test Job Descriptions:

### Fake Job (High Risk):
```
Urgent hiring! Work from home. Earn 50000 per month. 
No experience needed. Pay 500 registration fee. 
Contact on WhatsApp: 9876543210 or Gmail: hr@gmail.com
```

### Genuine Job (Low Risk):
```
Software Engineer position at TCS. 
Requirements: B.Tech/MCA with 60% marks.
Apply through official TCS careers portal.
Interview process: Aptitude test, Technical round, HR round.
Competitive salary with benefits.
```

---

## 📊 Expected Results:

- Fake job should show 70-90% risk score
- Genuine job should show 10-30% risk score
- Red flags will be highlighted
- ML prediction will show Fake/Genuine

---

## 🆘 Still Not Working?

1. Check if Python installed: `python --version`
2. Check if in correct folder: `dir` (should see app.py)
3. Try: `py app.py` instead of `python app.py`
4. Delete `instance` folder if exists
5. Restart computer and try again

---

## 📞 Need Help?

Take screenshot of error and check:
- Terminal/CMD output
- Browser console (F12)
- Error message

---

**Ready? Double-click START.bat now! 🚀**
