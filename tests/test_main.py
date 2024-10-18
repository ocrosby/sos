from sos.__main__ import fetch_data


def test_fetch_data(mocker):
    # Mock the TURNOUT_URL
    test_url = "http://example.com/data"

    # Mock the requests.get call to return a mock response
    mock_response = mocker.Mock()
    mock_response.content = b"mocked data"
    mocker.patch("requests.get", return_value=mock_response)

    # Call the fetch_data function
    result = fetch_data(test_url)

    # Assert that the result is as expected
    assert result == b"mocked data"
