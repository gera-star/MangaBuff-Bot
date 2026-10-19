from http.cookies import SimpleCookie

from buffy.social_auth import mangabuff_cookie_values


def test_cookie_export_keeps_only_mangabuff_domain_cookies():
    cookies = [
        {"name": "laravel_session", "value": "session-token", "domain": ".mangabuff.ru"},
        {"name": "XSRF-TOKEN", "value": "csrf-cookie", "domain": "mangabuff.ru"},
        {"name": "provider-session", "value": "external-token", "domain": ".google.com"},
    ]
    assert mangabuff_cookie_values(cookies) == {
        "laravel_session": "session-token",
        "XSRF-TOKEN": "csrf-cookie",
    }


def test_cookie_export_handles_simple_cookie():
    cookies = SimpleCookie()
    cookies.load("laravel_session=token; XSRF-TOKEN=csrf")
    assert mangabuff_cookie_values(cookies) == {
        "laravel_session": "token",
        "XSRF-TOKEN": "csrf",
    }


def test_cookie_export_handles_name_value_mapping():
    assert mangabuff_cookie_values({"laravel_session": "token"}) == {
        "laravel_session": "token"
    }


def test_cookie_export_skips_empty_and_foreign_cookie_values():
    cookies = [
        {"name": "empty", "value": "", "domain": "mangabuff.ru"},
        {"name": "foreign", "value": "value", "domain": "example.org"},
        {"name": "ok", "value": "session", "domain": "mangabuff.ru"},
    ]
    assert mangabuff_cookie_values(cookies) == {"ok": "session"}
