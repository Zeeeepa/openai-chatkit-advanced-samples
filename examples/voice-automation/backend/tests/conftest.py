"""Test configuration and fixtures."""

import sys
import os
from pathlib import Path

# Add the backend directory to the path so we can import app modules
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

# Import pytest for fixtures
import pytest

# No more mocks - using real chatkit and agents SDKs!
