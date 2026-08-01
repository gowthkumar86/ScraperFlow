import pytest
from unittest.mock import patch, Mock
from scraperflow.fetcher import fetch_page
from scraperflow.exceptions import TransientFetchError, PermanentFetchError


@pytest.fixture(autouse=True)
def no_retry_delay():
    """Disable sleep in retry decorator for all fetcher tests."""
    with patch("scraperflow.retry.time.sleep"):
        yield


class TestFetcherExceptionClassification:

    @patch("scraperflow.fetcher.requests.get")
    def test_raises_transient_on_5xx(self, mock_get):
        for code in [500, 502, 503, 504]:
            mock_get.return_value = Mock(status_code=code)
            with pytest.raises(TransientFetchError, match=str(code)):
                fetch_page("http://example.com")

    @patch("scraperflow.fetcher.requests.get")
    def test_raises_transient_on_429(self, mock_get):
        mock_get.return_value = Mock(status_code=429)
        with pytest.raises(TransientFetchError, match="429"):
            fetch_page("http://example.com")

    @patch("scraperflow.fetcher.requests.get")
    def test_raises_permanent_on_4xx(self, mock_get):
        for code in [400, 401, 403, 404, 410]:
            mock_get.return_value = Mock(status_code=code)
            with pytest.raises(PermanentFetchError, match=str(code)):
                fetch_page("http://example.com")

    @patch("scraperflow.fetcher.requests.get")
    def test_raises_transient_on_timeout(self, mock_get):
        import requests
        mock_get.side_effect = requests.Timeout("timed out")
        with pytest.raises(TransientFetchError, match="Timeout"):
            fetch_page("http://example.com")

    @patch("scraperflow.fetcher.requests.get")
    def test_raises_transient_on_connection_error(self, mock_get):
        import requests
        mock_get.side_effect = requests.ConnectionError("refused")
        with pytest.raises(TransientFetchError, match="Connection failed"):
            fetch_page("http://example.com")

    @patch("scraperflow.fetcher.requests.get")
    def test_returns_html_on_200(self, mock_get):
        mock_get.return_value = Mock(status_code=200, text="<html>ok</html>")
        result = fetch_page("http://example.com")
        assert result == "<html>ok</html>"
