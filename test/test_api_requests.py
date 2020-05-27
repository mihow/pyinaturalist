import os
import pytest
from unittest.mock import patch

import pyinaturalist
from pyinaturalist.api_requests import delete, get, post, put, request
from pyinaturalist.constants import MOCK_RESPONSE


# Just test that the wrapper methods call requests.request with the appropriate HTTP method
@pytest.mark.parametrize(
    "function, http_method",
    [(delete, "DELETE"), (get, "GET"), (post, "POST"), (put, "PUT")],
)
@patch("pyinaturalist.api_requests.request")
def test_http_methods(mock_request, function, http_method):
    function("https://url", param="value")
    mock_request.assert_called_with(http_method, "https://url", param="value")


# Test that the requests() wrapper passes along expected headers; just tests kwargs, not mock response
@pytest.mark.parametrize(
    "input_kwargs, expected_headers",
    [
        ({}, {"Accept": "application/json", "User-Agent": pyinaturalist.user_agent}),
        (
            {"user_agent": "CustomUA"},
            {"Accept": "application/json", "User-Agent": "CustomUA"},
        ),
        (
            {"access_token": "token"},
            {
                "Accept": "application/json",
                "User-Agent": pyinaturalist.user_agent,
                "Authorization": "Bearer token",
            },
        ),
    ],
)
@patch("pyinaturalist.api_requests.requests.request")
def test_request_headers(mock_request, input_kwargs, expected_headers):
    request("GET", "https://url", **input_kwargs)
    request_kwargs = mock_request.call_args[1]
    assert request_kwargs["headers"] == expected_headers


def test_request_dry_run_disabled(requests_mock):
    real_response = {"results": ["I'm a real response object!"]}
    requests_mock.get(
        "http://url", json={"results": ["I'm a real response object!"]}, status_code=200
    )

    assert request("GET", "http://url",).json() == real_response


@patch("pyinaturalist.api_requests.DRY_RUN_ENABLED")
@patch("pyinaturalist.api_requests.requests")
def test_request_dry_run_enabled__by_constant(mock_requests, mock_dry_run_enabled):
    assert request("GET", "http://url") == MOCK_RESPONSE
    assert mock_requests.call_count == 0


@patch("pyinaturalist.api_requests.getenv", return_value = 'True')
@patch("pyinaturalist.api_requests.requests")
def test_request_dry_run_enabled__by_envar(mock_requests, mock_os):
    # mock_os.getenv.return_value = 'True'
    assert request("GET", "http://url") == MOCK_RESPONSE
    assert mock_requests.call_count == 0
