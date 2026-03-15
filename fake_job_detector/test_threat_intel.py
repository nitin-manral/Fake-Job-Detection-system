"""Test script for Threat Intelligence feature"""
from app import app, db, ThreatIndicator, ScanHistory
from datetime import datetime

def test_threat_intelligence():
    """Test all threat intelligence components"""
    
    print("=" * 60)
    print("THREAT INTELLIGENCE FEATURE TEST")
    print("=" * 60)
    
    with app.app_context():
        # Test 1: Database Model
        print("\n[TEST 1] Database Model")
        try:
            db.create_all()
            print("✓ ThreatIndicator table created successfully")
        except Exception as e:
            print(f"✗ Error: {e}")
            return
        
        # Test 2: Create Sample Threat
        print("\n[TEST 2] Create Threat Indicator")
        try:
            test_threat = ThreatIndicator(
                indicator_type='email',
                indicator_value='test@gmail.com',
                threat_level='High',
                description='Test threat indicator',
                hit_count=1
            )
            db.session.add(test_threat)
            db.session.commit()
            print("✓ Threat indicator created successfully")
            print(f"  - Type: {test_threat.indicator_type}")
            print(f"  - Value: {test_threat.indicator_value}")
            print(f"  - Level: {test_threat.threat_level}")
        except Exception as e:
            print(f"✗ Error: {e}")
            db.session.rollback()
        
        # Test 3: Query Threats
        print("\n[TEST 3] Query Threat Indicators")
        try:
            threats = ThreatIndicator.query.all()
            print(f"✓ Found {len(threats)} threat indicator(s)")
            for threat in threats[:5]:  # Show first 5
                print(f"  - [{threat.threat_level}] {threat.indicator_type}: {threat.indicator_value}")
        except Exception as e:
            print(f"✗ Error: {e}")
        
        # Test 4: Update Hit Count
        print("\n[TEST 4] Update Hit Count")
        try:
            threat = ThreatIndicator.query.filter_by(indicator_value='test@gmail.com').first()
            if threat:
                threat.hit_count += 1
                threat.last_seen = datetime.utcnow()
                db.session.commit()
                print(f"✓ Hit count updated to {threat.hit_count}")
            else:
                print("✗ Test threat not found")
        except Exception as e:
            print(f"✗ Error: {e}")
            db.session.rollback()
        
        # Test 5: Threat Levels
        print("\n[TEST 5] Threat Level Distribution")
        try:
            from sqlalchemy import func
            levels = db.session.query(
                ThreatIndicator.threat_level,
                func.count(ThreatIndicator.id)
            ).group_by(ThreatIndicator.threat_level).all()
            
            print("✓ Threat level distribution:")
            for level, count in levels:
                print(f"  - {level}: {count}")
        except Exception as e:
            print(f"✗ Error: {e}")
        
        # Test 6: Recent High-Risk Scans
        print("\n[TEST 6] Recent High-Risk Scans")
        try:
            high_risk = ScanHistory.query.filter_by(risk_category='High').limit(5).all()
            print(f"✓ Found {len(high_risk)} high-risk scan(s)")
            for scan in high_risk:
                print(f"  - {scan.company_name} (Score: {scan.risk_score})")
        except Exception as e:
            print(f"✗ Error: {e}")
        
        # Test 7: API Data Format
        print("\n[TEST 7] API Data Format")
        try:
            indicators = ThreatIndicator.query.limit(3).all()
            feed = [{
                'type': ind.indicator_type,
                'value': ind.indicator_value,
                'level': ind.threat_level,
                'hits': ind.hit_count,
                'last_seen': ind.last_seen.strftime('%Y-%m-%d %H:%M')
            } for ind in indicators]
            
            print("✓ API format test successful")
            print(f"  Sample: {feed[0] if feed else 'No data'}")
        except Exception as e:
            print(f"✗ Error: {e}")
        
        # Test 8: Cleanup Test Data
        print("\n[TEST 8] Cleanup Test Data")
        try:
            test_threat = ThreatIndicator.query.filter_by(indicator_value='test@gmail.com').first()
            if test_threat:
                db.session.delete(test_threat)
                db.session.commit()
                print("✓ Test data cleaned up")
        except Exception as e:
            print(f"✗ Error: {e}")
            db.session.rollback()
        
        # Summary
        print("\n" + "=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        
        total_threats = ThreatIndicator.query.count()
        total_scans = ScanHistory.query.count()
        high_risk_scans = ScanHistory.query.filter_by(risk_category='High').count()
        
        print(f"Total Threat Indicators: {total_threats}")
        print(f"Total Scans: {total_scans}")
        print(f"High-Risk Scans: {high_risk_scans}")
        
        if total_threats == 0:
            print("\n⚠️  No threat indicators found!")
            print("   Run: python init_threats.py")
        else:
            print("\n✅ Threat Intelligence system is working!")
        
        print("\n" + "=" * 60)
        print("Next Steps:")
        print("1. Run 'python init_threats.py' for sample data")
        print("2. Start app: 'python app.py'")
        print("3. Visit: http://127.0.0.1:5000/threat-intelligence")
        print("4. Test API: http://127.0.0.1:5000/api/threat-feed")
        print("=" * 60)

if __name__ == '__main__':
    test_threat_intelligence()
