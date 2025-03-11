"""Tests demonstrating fixture usage."""


def test_fixture_numbers(test_fixture):
    """Test working with the numbers list from the fixture."""
    numbers = test_fixture["numbers"]
    assert len(numbers) == 5
    assert sum(numbers) == 15
    assert all(isinstance(n, int) for n in numbers)


def test_fixture_text(test_fixture):
    """Test working with the text string from the fixture."""
    text = test_fixture["text"]
    assert isinstance(text, str)
    assert text == "hello from fixture"
    assert len(text) > 0


def test_fixture_config(test_fixture):
    """Test working with the config dictionary from the fixture."""
    config = test_fixture["config"]
    assert config["enabled"] is True
    assert config["max_value"] == 100
    assert len(config) == 2
