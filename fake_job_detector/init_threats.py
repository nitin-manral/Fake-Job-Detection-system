"""Initialize sample threat indicators for demonstration"""
from app import app, db, ThreatIndicator
from datetime import datetime, timedelta
import random

def init_sample_threats():
    with app.app_context():
        # Clear existing indicators
        ThreatIndicator.query.delete()
        
        # Sample threat indicators
        threats = [
            {
                'type': 'email',
                'value': 'hr.quickjobs@gmail.com',
                'level': 'Critical',
                'desc': 'Known scam email - multiple fraud reports',
                'hits': 45
            },
            {
                'type': 'email',
                'value': 'recruitment@yahoo.com',
                'level': 'High',
                'desc': 'Personal email used for fake recruitment',
                'hits': 32
            },
            {
                'type': 'domain',
                'value': 'quickcash-jobs.xyz',
                'level': 'Critical',
                'desc': 'Fraudulent job portal - advance fee scam',
                'hits': 67
            },
            {
                'type': 'domain',
                'value': 'homejobs-india.com',
                'level': 'High',
                'desc': 'Suspicious domain with multiple complaints',
                'hits': 28
            },
            {
                'type': 'keyword',
                'value': 'urgent, registration fee, guaranteed income',
                'level': 'Critical',
                'desc': 'High-risk keyword combination detected',
                'hits': 89
            },
            {
                'type': 'email',
                'value': 'jobs.hiring@hotmail.com',
                'level': 'Medium',
                'desc': 'Free email service used for recruitment',
                'hits': 15
            },
            {
                'type': 'domain',
                'value': 'dataentry-work.online',
                'level': 'High',
                'desc': 'Data entry scam website',
                'hits': 41
            },
            {
                'type': 'keyword',
                'value': 'whatsapp, deposit, immediate joining',
                'level': 'High',
                'desc': 'Suspicious communication pattern',
                'hits': 53
            }
        ]
        
        for threat in threats:
            days_ago = random.randint(1, 30)
            indicator = ThreatIndicator(
                indicator_type=threat['type'],
                indicator_value=threat['value'],
                threat_level=threat['level'],
                description=threat['desc'],
                hit_count=threat['hits'],
                first_seen=datetime.utcnow() - timedelta(days=days_ago),
                last_seen=datetime.utcnow() - timedelta(hours=random.randint(1, 48))
            )
            db.session.add(indicator)
        
        db.session.commit()
        print(f"✓ Initialized {len(threats)} threat indicators")

if __name__ == '__main__':
    init_sample_threats()
