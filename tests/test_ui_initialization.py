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


def test_add_account_and_close_actions_are_reachable_and_report_failures():
    html_path = Path(__file__).resolve().parents[1] / "buffy" / "ui" / "index.html"
    source = html_path.read_text(encoding="utf-8")

    assert '>＋ Добавить аккаунт</button>' in source
    assert '$("#acc-change").addEventListener("click", async () => {' in source
    assert 'wizard.open(1);' in source
    assert 'async function closeAs(action)' in source
    assert 'await api.quit_app()' in source
    assert 'toast("Не удалось выполнить команду: " + (e?.message || e), "err");' in source
