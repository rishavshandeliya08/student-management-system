import sys
import os

# Add parent directory to path so api/index.py can import app and models from root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app
