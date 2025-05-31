# tests/pytest/__init__.py

import pytest

@pytest.fixture(scope="session")
def sample_fixture():
    return "shared value"
