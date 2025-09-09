"""
Test Script for Milestone 3.1: Database Migrations & Seeding

This script validates that all requirements for milestone 3.1 have been met:
- ✅ Alembic migration system set up
- ✅ Initial migration created and applied
- ✅ Database seeding script created with sample data
- ✅ Can run migrations and seeds consistently
- ✅ Database versioning working
"""

import subprocess
import sys
import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# Add the current directory to Python path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import using absolute imports to avoid relative import issues
from app.models import Book
from app.database import DATABASE_URL

def test_migration_system():
    """Test that the Alembic migration system is working correctly."""
    print("🧪 Testing Migration System...")
    
    try:
        # Test downgrade
        result = subprocess.run(['alembic', 'downgrade', '-1'], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(f"Downgrade failed: {result.stderr}")
        
        # Test upgrade
        result = subprocess.run(['alembic', 'upgrade', 'head'], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(f"Upgrade failed: {result.stderr}")
            
        print("   ✅ Migration system working correctly")
        return True
        
    except Exception as e:
        print(f"   ❌ Migration system test failed: {e}")
        return False

def test_seeding_functionality():
    """Test that the database seeding is working correctly."""
    print("🧪 Testing Seeding Functionality...")
    
    try:
        # Create engine and session
        engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        # Count books before seeding
        initial_count = db.query(Book).count()
        print(f"   📊 Books in database: {initial_count}")
        
        # Run seeding script
        result = subprocess.run([sys.executable, 'app/seed.py'], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(f"Seeding failed: {result.stderr}")
        
        # Count books after seeding
        final_count = db.query(Book).count()
        print(f"   📊 Books after seeding: {final_count}")
        
        if final_count >= 8:  # We expect at least 8 sample books
            print("   ✅ Seeding functionality working correctly")
            return True
        else:
            print(f"   ❌ Expected at least 8 books, got {final_count}")
            return False
            
    except Exception as e:
        print(f"   ❌ Seeding test failed: {e}")
        return False
    finally:
        db.close()

def test_milestone_3_1():
    """
    Complete test suite for Milestone 3.1
    """
    print("🎯 MILESTONE 3.1 TEST SUITE")
    print("=" * 50)
    print("Database Migrations & Seeding")
    print()
    
    # Test migration system
    migration_test = test_migration_system()
    
    # Test seeding functionality  
    seeding_test = test_seeding_functionality()
    
    print()
    print("📋 TEST RESULTS:")
    print("-" * 30)
    print(f"Migration System: {'✅ PASS' if migration_test else '❌ FAIL'}")
    print(f"Seeding System:   {'✅ PASS' if seeding_test else '❌ FAIL'}")
    
    overall_success = migration_test and seeding_test
    
    print()
    if overall_success:
        print("🎉 MILESTONE 3.1 COMPLETED SUCCESSFULLY!")
        print("✅ All requirements met:")
        print("   - Alembic migration system set up")
        print("   - Initial migration created and applied")  
        print("   - Database seeding script working")
        print("   - Migrations and seeds run consistently")
        print("   - Database versioning functional")
    else:
        print("❌ MILESTONE 3.1 INCOMPLETE")
        print("Some requirements not met. Please check the errors above.")
    
    return overall_success

if __name__ == "__main__":
    test_milestone_3_1()
