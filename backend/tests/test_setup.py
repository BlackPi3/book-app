#!/usr/bin/env python3
"""
Test script to verify MILESTONE 1.1 completion
This script tests that all dependencies are properly installed and importable.
"""

def test_imports():
    """Test that all required packages can be imported successfully."""
    import fastapi
    import sqlalchemy
    import pydantic
    import uvicorn
    import alembic
    import pytest
    import httpx

    print("✅ All imports successful!")
    print(f"FastAPI version: {fastapi.__version__}")
    print(f"SQLAlchemy version: {sqlalchemy.__version__}")
    print(f"Pydantic version: {pydantic.__version__}")
    print(f"Uvicorn version: {uvicorn.__version__}")
    print(f"Alembic version: {alembic.__version__}")
    print(f"Pytest version: {pytest.__version__}")
    print(f"HTTPX version: {httpx.__version__}")

    # All imports successful if we reach here
    assert True

def test_directory_structure():
    """Test that the project structure follows layered architecture."""
    import os

    base_path = "/Users/parham/Desktop/Job/interview/4- DHC/book-app"

    # Check for required directories
    required_dirs = [
        "backend/app",
        "backend/app/repositories",
        "backend/app/services",
        "backend/app/api",
        "backend/tests",
        "frontend",
        "docker"
    ]

    # Check for required files
    required_files = [
        "backend/app/models.py",
        "backend/app/schemas.py",
        "backend/app/database.py",
        "backend/app/main.py"
    ]

    missing_dirs = []
    missing_files = []

    # Check directories
    for dir_path in required_dirs:
        full_path = os.path.join(base_path, dir_path)
        if not os.path.exists(full_path):
            missing_dirs.append(dir_path)

    # Check files
    for file_path in required_files:
        full_path = os.path.join(base_path, file_path)
        if not os.path.exists(full_path):
            missing_files.append(file_path)

    missing_items = missing_dirs + missing_files

    if missing_items:
        print(f"❌ Missing directories: {missing_dirs}")
        print(f"❌ Missing files: {missing_files}")
        assert False, f"Missing required items: {missing_items}"
    else:
        print("✅ All required directories exist!")
        print("✅ All required files exist!")
        print("✅ Project structure follows layered architecture!")
        assert True

if __name__ == "__main__":
    print("🧪 Testing MILESTONE 1.1 completion...")
    print("=" * 50)

    try:
        test_imports()
        imports_ok = True
    except Exception as e:
        print(f"❌ Import test failed: {e}")
        imports_ok = False

    print()

    try:
        test_directory_structure()
        structure_ok = True
    except Exception as e:
        print(f"❌ Directory structure test failed: {e}")
        structure_ok = False

    print("\n" + "=" * 50)
    if imports_ok and structure_ok:
        print("🎉 MILESTONE 1.1 SUCCESSFULLY COMPLETED!")
        print("✅ Ready to proceed to MILESTONE 1.2")
    else:
        print("❌ MILESTONE 1.1 needs fixes before proceeding")
