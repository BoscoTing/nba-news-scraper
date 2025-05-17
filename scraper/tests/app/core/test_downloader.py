from unittest.mock import Mock, patch

import pytest
import requests

from app.core.downloader import Downloader

@pytest.fixture
def downloader():
    return Downloader()

def test_get_headers(downloader):
    """
    Test that headers are returned with expected keys
    """
    headers = downloader._get_headers()
    
    assert isinstance(headers, dict)
    assert 'User-Agent' in headers
    assert 'Accept' in headers
    assert 'Accept-Language' in headers
    
    assert isinstance(headers['User-Agent'], str)
    
    assert headers['Accept'] == 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    assert headers['Accept-Language'] == 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7'

@patch('requests.get')
def test_download_success(mock_get, downloader):
    """
    Mock successful response
    """
    mock_response = Mock()
    mock_response.text = "Test HTML content"
    mock_get.return_value = mock_response
    
    result = downloader.download("https://example.com")
    
    assert result == "Test HTML content"
    mock_get.assert_called_once()

    call_args = mock_get.call_args[1]
    assert 'headers' in call_args
    assert isinstance(call_args['headers'], dict)

@patch('requests.get')
def test_download_failure(mock_get, downloader):
    """
    Mock failed request with the correct exception type
    """
    mock_get.side_effect = requests.exceptions.RequestException("Connection error")
    
    with pytest.raises(requests.exceptions.RequestException) as exc_info:
        downloader.download("https://example.com")
    
    assert "Connection error" in str(exc_info.value)
    assert mock_get.call_count == 3

@patch('requests.get')
def test_download_retry_success(mock_get, downloader):
    """
    Mock first two attempts failing, third succeeding
    """
    mock_response = Mock()
    mock_response.text = "Test HTML content"
    mock_get.side_effect = [
        requests.exceptions.RequestException("First attempt failed"),
        requests.exceptions.RequestException("Second attempt failed"),
        mock_response,
    ]
    
    result = downloader.download("https://example.com")
    
    assert result == "Test HTML content"
    assert mock_get.call_count == 3
