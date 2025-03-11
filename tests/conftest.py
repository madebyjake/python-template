"""Pytest configuration."""

import sys
from pathlib import Path

import pytest

src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))


@pytest.fixture
def test_fixture():
    """Fixture providing test data."""
    return {
        "numbers": [1, 2, 3, 4, 5],
        "text": "hello from fixture",
        "config": {"enabled": True, "max_value": 100},
    }
