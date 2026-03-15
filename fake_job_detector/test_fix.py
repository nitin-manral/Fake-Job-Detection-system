#!/usr/bin/env python3
"""
Test script to verify the analyze page fixes
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db, init_db

def test_analyze_route():
    """Test the analyze route with various scenarios"""
    with app.test_client() as client:
        with app.app_context():
            # Initialize database
            init_db()
            
            print("Testing analyze route...")
            
            # Test 1: GET request (should load page without errors)
            print("1. Testing GET request...")
            response = client.get('/analyze')
            assert response.status_code == 200
            assert b'UndefinedError' not in response.data
            assert b'Job Analyzer' in response.data
            print("   [OK] GET request successful")
            
            # Test 2: POST request with minimal data
            print("2. Testing POST with minimal data...")
            response = client.post('/analyze', data={
                'company_name': 'Test Company',
                'job_description': 'Software developer position'
            })
            assert response.status_code == 200
            # Check that the response contains analysis results
            assert b'Investigation Report' in response.data or b'Risk Assessment' in response.data
            assert b'UndefinedError' not in response.data
            print("   [OK] POST with minimal data successful")
            
            # Test 3: POST request with suspicious content
            print("3. Testing POST with suspicious content...")
            response = client.post('/analyze', data={
                'company_name': 'QuickCash Ltd',
                'job_description': 'Urgent hiring! Easy money, work from home, no experience required. Pay registration fee.',
                'hr_email': 'hr@gmail.com',
                'job_link': 'http://newdomain.com/jobs'
            })
            assert response.status_code == 200
            # Check that the response contains analysis results
            assert b'Investigation Report' in response.data or b'Risk Assessment' in response.data
            assert b'UndefinedError' not in response.data
            print("   [OK] POST with suspicious content successful")
            
            # Test 4: POST request with empty data
            print("4. Testing POST with empty data...")
            response = client.post('/analyze', data={
                'company_name': '',
                'job_description': ''
            })
            assert response.status_code == 200
            # Should not crash even with empty data
            assert b'UndefinedError' not in response.data
            print("   [OK] POST with empty data successful")
            
            print("All tests passed! [OK]")

if __name__ == '__main__':
    test_analyze_route()
    print("Fix verification complete!")