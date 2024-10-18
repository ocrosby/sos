import pytest

from sos.main import fetch_data


def test_fetch_data(mocker):
    # Mock the TURNOUT_URL
    TURNOUT_URL = "http://example.com/data"

    # Mock the requests.get call to return a mock response
    mock_response = mocker.Mock()
    mock_response.content = b"mocked data"
    mocker.patch("requests.get", return_value=mock_response)

    # Call the fetch_data function
    result = fetch_data(TURNOUT_URL)

    # Assert that the result is as expected
    assert result == b"mocked data"
