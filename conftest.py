"""
Root conftest.py for BookApp project

This file configures the Python path for all tests to resolve import issues.
It ensures that all test files can properly import from the app module.
"""

import sys
import os
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent / "backend"
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

# Also add the project root to Python path
project_root = Path(__file__).parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Set PYTHONPATH environment variable for IDE recognition
os.environ['PYTHONPATH'] = f"{backend_dir}:{project_root}:{os.environ.get('PYTHONPATH', '')}"
