import pytest
from utils.validation import validate_profile_data, normalize_profile_data
from unittest.mock import patch


@pytest.mark.parametrize("first, last, sid, expected",
    [
        # Valid partition
        ("Alice", "Smith", "12345678", None),
        # Missing first_name
        ("", "Smith", "12345678", "All fields are required."),
        # Missing last_name
        ("Alice", "", "12345678", "All fields are required."),
        # Missing student_id
        ("Alice", "Smith", "", "All fields are required."),
        # None value
        (None, "Smith", "12345678", "All fields are required."),
        # All empty
        ("", "", "", "All fields are required."),
        # Whitespace-only first_name
        ("   ", "Smith", "12345678", None),  # Whitespace is truthy, so passes
        # Whitespace-only last_name
        ("Alice", "   ", "12345678", None),
        # Whitespace-only student_id
        ("Alice", "Smith", "   ", None),
        # All whitespace
        ("   ", "   ", "   ", None),
        # Valid with leading/trailing spaces
        (" Alice ", " Smith ", " 12345678 ", None),
        # Mixed None and empty
        (None, "", "12345678", "All fields are required."),
        ("Alice", None, "12345678", "All fields are required."),
        ("Alice", "Smith", None, "All fields are required."),
    ]
)
def test_validate(first, last, sid, expected):
    assert validate_profile_data(first, last, sid) == expected


@pytest.mark.parametrize("first, last, sid, expected",
    [
        # Normal case
        ("Alice", "Smith", "12345678", {"first_name": "Alice", "last_name": "Smith", "student_id": "12345678"}),
        # With leading/trailing spaces
        (" Alice ", " Smith ", " 12345678 ", {"first_name": "Alice", "last_name": "Smith", "student_id": "12345678"}),
        # None values
        (None, None, None, {"first_name": "", "last_name": "", "student_id": ""}),
        # Empty strings
        ("", "", "", {"first_name": "", "last_name": "", "student_id": ""}),
        # Integer student_id
        ("Alice", "Smith", 12345678, {"first_name": "Alice", "last_name": "Smith", "student_id": "12345678"}),
    ]
)
def test_normalize(first, last, sid, expected):
    assert normalize_profile_data(first, last, sid) == expected