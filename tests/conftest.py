"""
These settings get applied to all tests in the same directory
"""
import sys

from pathlib import Path

# Add project root to sys path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.append(str(PROJECT_ROOT))
