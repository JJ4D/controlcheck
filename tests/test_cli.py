import runpy

import pytest

from controlcheck import __version__
from controlcheck.cli import main


def test_version_flag_prints_version_and_exits_zero(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as exc_info:
        main(["--version"])

    assert exc_info.value.code == 0
    assert capsys.readouterr().out.strip() == f"controlcheck {__version__}"


def test_no_arguments_prints_help(capsys: pytest.CaptureFixture[str]) -> None:
    assert main([]) == 0
    assert "usage: controlcheck" in capsys.readouterr().out


def test_unknown_argument_is_a_usage_error(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as exc_info:
        main(["--no-such-flag"])

    assert exc_info.value.code == 2
    assert "unrecognized arguments" in capsys.readouterr().err


def test_python_dash_m_entry_point(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("sys.argv", ["controlcheck", "--version"])

    with pytest.raises(SystemExit) as exc_info:
        runpy.run_module("controlcheck", run_name="__main__")

    assert exc_info.value.code == 0
