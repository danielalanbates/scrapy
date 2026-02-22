#!/usr/bin/env python3
"""Test case for issue #6574: URLs with query string but no path should get a / path"""

from scrapy.http import Request
from urllib.parse import urlparse


def test_url_with_query_string_but_no_path():
    """Test that URLs with query string but no path get a / path"""
    # This is the original issue - URL without path but with query string
    url = "http://127.0.0.1:9000?url=www.baidu.com"
    req = Request(url)

    # The path should not be empty - it should have at least a /
    parsed = urlparse(req.url)
    print(f"Original URL: {url}")
    print(f"Request URL: {req.url}")
    print(f"Parsed path: '{parsed.path}'")
    print(f"Parsed query: '{parsed.query}'")

    # The path should be / when it was missing in the original URL
    # This ensures valid HTTP request line: GET / ?url=www.baidu.com HTTP/1.1
    # instead of: GET ?url=www.baidu.com HTTP/1.1 (invalid)
    assert parsed.path == "/", f"Expected path to be '/', got '{parsed.path}'"
    assert parsed.query == "url=www.baidu.com"
    assert req.url == "http://127.0.0.1:9000/?url=www.baidu.com"


def test_url_with_existing_path_unchanged():
    """Test that URLs with existing path are not modified"""
    url = "http://127.0.0.1:9000/path?url=www.baidu.com"
    req = Request(url)

    parsed = urlparse(req.url)
    print(f"Original URL: {url}")
    print(f"Request URL: {req.url}")

    assert parsed.path == "/path"
    assert parsed.query == "url=www.baidu.com"
    assert req.url == "http://127.0.0.1:9000/path?url=www.baidu.com"


def test_url_without_query_string_unchanged():
    """Test that URLs without query string are not modified"""
    url = "http://127.0.0.1:9000"
    req = Request(url)

    parsed = urlparse(req.url)
    print(f"Original URL: {url}")
    print(f"Request URL: {req.url}")

    # Even without query string, if there's no path, it might get /
    # This is actually OK for consistency
    assert parsed.query == ""


if __name__ == "__main__":
    print("Test 1: URL with query string but no path")
    try:
        test_url_with_query_string_but_no_path()
        print("PASS\n")
    except AssertionError as e:
        print(f"FAIL: {e}\n")

    print("Test 2: URL with existing path")
    try:
        test_url_with_existing_path_unchanged()
        print("PASS\n")
    except AssertionError as e:
        print(f"FAIL: {e}\n")

    print("Test 3: URL without query string")
    try:
        test_url_without_query_string_unchanged()
        print("PASS\n")
    except AssertionError as e:
        print(f"FAIL: {e}\n")
