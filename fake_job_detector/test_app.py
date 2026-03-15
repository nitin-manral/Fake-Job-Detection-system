print("Testing app.py...")
try:
    from app import app, db
    print("✓ App imported successfully")
    
    with app.app_context():
        db.create_all()
        print("✓ Database created successfully")
    
    print("\n✅ No errors! App is ready to run.")
    print("\nRun: python app.py")
    
except Exception as e:
    print(f"\n❌ Error found: {e}")
    import traceback
    traceback.print_exc()
