"""Test configuration and fixtures."""

import sys
from unittest.mock import MagicMock

# Mock chatkit module
chatkit_mock = MagicMock()
chatkit_mock.Server = MagicMock
chatkit_mock.store = MagicMock()
chatkit_mock.store.Store = object
chatkit_mock.types = MagicMock()
chatkit_mock.types.ThreadContext = MagicMock
chatkit_mock.types.ThreadMetadata = MagicMock
sys.modules['chatkit'] = chatkit_mock

# Mock agents module
agents_mock = MagicMock()
agents_mock.Agent = MagicMock
sys.modules['agents'] = agents_mock

