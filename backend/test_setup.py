#!/usr/bin/env python3
"""
Test script to verify MILESTONE 1.1 completion
This script tests that all dependencies are properly installed and importable.
"""

def test_imports():
    """Test that all required packages can be imported successfully."""
    try:
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

        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_directory_structure():
    """Test that the project structure follows layered architecture."""
    import os

    base_path = "/Users/parham/Desktop/Job/interview/4- DHC/book-app"
    required_dirs = [
        "backend/app",
        "backend/app/models",
        "backend/app/schemas",
        "backend/app/repositories",
        "backend/app/services",
        "backend/app/api",
        "backend/tests",
        "frontend",
        "docker"
    ]

    missing_dirs = []
    for dir_path in required_dirs:
        full_path = os.path.join(base_path, dir_path)
        if not os.path.exists(full_path):
            missing_dirs.append(dir_path)

    if missing_dirs:
        print(f"❌ Missing directories: {missing_dirs}")
        return False
    else:
        print("✅ All required directories exist!")
        print("✅ Project structure follows layered architecture!")
        return True

if __name__ == "__main__":
    print("🧪 Testing MILESTONE 1.1 completion...")
    print("=" * 50)

    imports_ok = test_imports()
    print()
    structure_ok = test_directory_structure()

    print("\n" + "=" * 50)
    if imports_ok and structure_ok:
        print("🎉 MILESTONE 1.1 SUCCESSFULLY COMPLETED!")
        print("✅ Ready to proceed to MILESTONE 1.2")
    else:
        print("❌ MILESTONE 1.1 needs fixes before proceeding")
