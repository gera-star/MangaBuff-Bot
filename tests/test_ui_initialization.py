from pathlib import Path


def test_social_login_buttons_use_a_collection_and_do_not_abort_ui_boot():
    """All provider buttons must be wired; one-element querySelector broke all later JS."""
    html_path = Path(__file__).resolve().parents[1] / "buffy" / "ui" / "index.html"
    source = html_path.read_text(encoding="utf-8")

    assert 'const socialLoginButtons = $$("[data-social-login]");' in source
    assert 'if (!boot.has_credentials) wizard.open(1);' in source
    assert 'else if (!boot.onboarded) wizard.open(2);' in source
    assert 'socialLoginButtons.forEach((button) => {' in source
    assert '$("#w-login").addEventListener("click", doLogin);' in source
    assert 'window.askClose = () =>' in source
    assert '$("#close-quit").addEventListener("click", () => closeAs("quit"));' in source
