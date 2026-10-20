from pathlib import Path


def test_full_exit_schedules_window_destruction_and_hard_exit_fallback():
    app_path = Path(__file__).resolve().parents[1] / "buffy" / "app.py"
    source = app_path.read_text(encoding="utf-8")

    assert "threading.Timer(0.2, destroy_window)" in source
    assert "threading.Timer(10.0, force_exit)" in source
    assert 'if state["quitting"] or action == "quit":' in source
