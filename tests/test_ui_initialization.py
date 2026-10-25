from pathlib import Path


def test_social_login_buttons_use_a_collection_and_do_not_abort_ui_boot():
    """Social provider controls must all be wired using the current upstream API."""
    html_path = Path(__file__).resolve().parents[1] / "buffy" / "ui" / "index.html"
    source = html_path.read_text(encoding="utf-8")

    assert '$$("[data-social]")' in source
    assert 'const r = await api.social_login(b.dataset.social);' in source
    assert 'if (!boot.onboarded) wizard.open(boot.has_credentials ? 2 : 0);' in source
    assert '$("#w-login").addEventListener("click", doLogin);' in source
    assert 'window.askClose = () =>' in source
    assert '$("#close-quit").addEventListener("click", () => closeAs("quit"));' in source


def test_add_account_and_close_actions_are_reachable_and_report_failures():
    html_path = Path(__file__).resolve().parents[1] / "buffy" / "ui" / "index.html"
    source = html_path.read_text(encoding="utf-8")

    assert '>＋ Добавить аккаунт</button>' in source
    assert source.count('$("#acc-change").addEventListener("click", async () => {') == 1
    assert "await api.logout();" not in source
    assert "Keep the current login until the new login succeeds." in source
    assert 'wizard.open(1);' in source
    assert 'async function closeAs(action)' in source
    assert 'await api.quit_app()' in source
    assert 'toast("Не удалось выполнить команду: " + (e?.message || e), "err");' in source
