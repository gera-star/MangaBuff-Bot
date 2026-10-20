from buffy.social_auth import is_mangabuff_url, social_login_url


def test_all_four_social_login_urls_are_whitelisted():
    assert social_login_url("vkid") == "https://mangabuff.ru/login/redirect/vkid"
    assert social_login_url("discord") == "https://mangabuff.ru/login/redirect/discord"
    assert social_login_url("yandex") == "https://mangabuff.ru/login/redirect/yandex"
    assert social_login_url("google") == "https://mangabuff.ru/login/redirect/google"


def test_social_login_url_rejects_unknown_provider():
    try:
        social_login_url("unknown")
    except ValueError:
        pass
    else:
        raise AssertionError("unsupported provider must be rejected")


def test_mangabuff_url_requires_https_and_the_real_host():
    assert is_mangabuff_url("https://mangabuff.ru/mine")
    assert is_mangabuff_url("https://auth.mangabuff.ru/login")
    assert not is_mangabuff_url("http://mangabuff.ru/mine")
    assert not is_mangabuff_url("https://mangabuff.ru.example.org/")
