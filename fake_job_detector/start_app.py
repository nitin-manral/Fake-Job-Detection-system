#!/usr/bin/env python3
"""
AI Fake Job Detector - Startup Script
This script initializes and runs the Flask application with proper error handling.
"""

import os
import sys
import subprocess

def check_dependencies():
    """Check if all required dependencies are installed."""
    try:
        import flask
        import flask_sqlalchemy
        import sklearn
        import whois
        import reportlab
        print("✓ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"✗ Missing dependency: {e}")
        print("Please install dependencies using: pip install -r requirements.txt")
        return False

def setup_environment():
    """Set up environment variables and configuration."""
    os.environ.setdefault('FLASK_ENV', 'development')
    os.environ.setdefault('FLASK_DEBUG', '1')
    print("✓ Environment configured")

def main():
    """Main startup function."""
    print("=" * 50)
    print("AI Fake Job Detector - Starting Application")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Setup environment
    setup_environment()
    
    # Import and run the Flask app
    try:
        from app import app, init_db
        
        print("✓ Flask application imported successfully")
        
        # Initialize database
        print("Initializing database...")
        init_db()
        
        print("✓ Database initialized")
        print("=" * 50)
        print("Starting Flask development server...")
        print("Application will be available at: http://127.0.0.1:5000")
        print("Admin login: username=admin, password=admin123")
        print("Press Ctrl+C to stop the server")
        print("=" * 50)
        
        # Run the Flask app
        app.run(host='127.0.0.1', port=5000, debug=True)
        
    except ImportError as e:
        print(f"✗ Error importing Flask app: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Error starting application: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()