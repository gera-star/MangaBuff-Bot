"""Helpers for the MangaBuff website's social-login redirects and cookie export."""
from __future__ import annotations

from urllib.parse import urlsplit


SOCIAL_PROVIDERS = {
    "vkid": "ВКонтакте",
    "discord": "Discord",
    "yandex": "Яндекс",
    "google": "Google",
}


def social_login_url(provider: str) -> str:
    """Return a known MangaBuff redirect URL; never accept an arbitrary target."""
    provider = str(provider or "").strip().lower()
    if provider not in SOCIAL_PROVIDERS:
        raise ValueError("Unsupported MangaBuff social-login provider")
    return f"https://mangabuff.ru/login/redirect/{provider}"


def is_mangabuff_url(url: str) -> bool:
    """Only trust HTTPS pages on MangaBuff itself or one of its subdomains."""
    try:
        parsed = urlsplit(str(url or ""))
        host = (parsed.hostname or "").lower().rstrip(".")
        return parsed.scheme.lower() == "https" and (
            host == "mangabuff.ru" or host.endswith(".mangabuff.ru")
        )
    except (TypeError, ValueError):
        return False


def _allowed_cookie_domain(domain: str) -> bool:
    domain = str(domain or "").lower().strip().lstrip(".").rstrip(".")
    return not domain or domain == "mangabuff.ru" or domain.endswith(".mangabuff.ru")


def _value_and_domain(name, value, domain=""):
    """Normalize a cookie morsel / Cookie object into a safe name-value pair."""
    if hasattr(value, "value"):
        cookie_value = value.value
        try:
            domain = domain or value["domain"]
        except (KeyError, TypeError, AttributeError):
            domain = domain or getattr(value, "domain", "")
    else:
        cookie_value = value
    if not isinstance(name, str) or not name or cookie_value is None:
        return None
    if not _allowed_cookie_domain(domain):
        return None
    if not isinstance(cookie_value, str):
        cookie_value = str(cookie_value)
    if not cookie_value:
        return None
    return name, cookie_value


def mangabuff_cookie_values(raw_cookies) -> dict[str, str]:
    """Convert pywebview cookie results to a name-value map for MangaBuff only.

    pywebview versions/platforms may return Cookie objects, SimpleCookie objects,
    or dictionaries. Host-only cookies have no domain attribute and are retained;
    explicitly foreign-domain cookies are discarded.
    """
    result: dict[str, str] = {}
    if raw_cookies is None:
        return result

    if isinstance(raw_cookies, dict):
        if "name" in raw_cookies:
            items = [raw_cookies]
        else:
            # A name -> value mapping is already scoped by the caller to the
            # currently loaded MangaBuff page.
            items = [raw_cookies]
    else:
        try:
            items = list(raw_cookies)
        except TypeError:
            items = [raw_cookies]

    for item in items:
        if isinstance(item, dict):
            if "name" in item:
                pair = _value_and_domain(
                    item.get("name"), item.get("value"), item.get("domain", "")
                )
                if pair:
                    result[pair[0]] = pair[1]
            else:
                domain = item.get("domain", "")
                for name, value in item.items():
                    pair = _value_and_domain(name, value, domain)
                    if pair:
                        result[pair[0]] = pair[1]
            continue

        if hasattr(item, "name") and hasattr(item, "value"):
            pair = _value_and_domain(
                getattr(item, "name", None),
                getattr(item, "value", None),
                getattr(item, "domain", ""),
            )
            if pair:
                result[pair[0]] = pair[1]
            continue

        if hasattr(item, "items"):
            domain = ""
            try:
                domain = item["domain"]
            except (KeyError, TypeError, AttributeError):
                domain = getattr(item, "domain", "")
            try:
                pairs = item.items()
            except Exception:
                continue
            for name, value in pairs:
                pair = _value_and_domain(name, value, domain)
                if pair:
                    result[pair[0]] = pair[1]

    return result
