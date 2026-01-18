import sys
from unittest.mock import patch, MagicMock
from pathlib import Path
import pytest
from depscripter.cli import main

def test_cli_file_not_found(tmp_path):
    with patch("sys.argv", ["depscripter", str(tmp_path / "missing.py")]):
        with pytest.raises(SystemExit):
            main()

def test_cli_successful_run(tmp_path, capsys):
    f = tmp_path / "script.py"
    f.write_text("import requests", encoding="utf-8")
    
    with patch("sys.argv", ["depscripter", str(f), "--no-pin"]):
        with patch("depscripter.cli.scan_imports", return_value={"requests"}), \
             patch("depscripter.cli.resolve_packages", return_value={"requests": None}), \
             patch("depscripter.cli.generate_script_metadata", return_value="# /// metadata"), \
             patch("depscripter.cli.inject_metadata", return_value="# /// metadata\nimport requests"):
             
             main()
             
    captured = capsys.readouterr()
    assert "# /// metadata" in captured.out

def test_cli_in_place(tmp_path):
    f = tmp_path / "script.py"
    f.write_text("import requests", encoding="utf-8")
    
    with patch("sys.argv", ["depscripter", str(f), "--in-place", "--no-pin"]):
        with patch("depscripter.cli.scan_imports", return_value={"requests"}), \
             patch("depscripter.cli.resolve_packages", return_value={"requests": None}), \
             patch("depscripter.cli.generate_script_metadata", return_value="# /// metadata"), \
             patch("depscripter.cli.inject_metadata", return_value="# /// metadata\nimport requests"):
             
             main()
    
    assert f.read_text(encoding="utf-8") == "# /// metadata\nimport requests"

def test_cli_output_option(tmp_path):
    f = tmp_path / "script.py"
    f.write_text("import requests", encoding="utf-8")
    out = tmp_path / "output.py"
    
    with patch("sys.argv", ["depscripter", str(f), "-o", str(out), "--no-pin"]):
        with patch("depscripter.cli.scan_imports", return_value={"requests"}), \
             patch("depscripter.cli.resolve_packages", return_value={"requests": None}), \
             patch("depscripter.cli.generate_script_metadata", return_value="# /// metadata"), \
             patch("depscripter.cli.inject_metadata", return_value="# /// metadata\nimport requests"):
             
             main()
    
    assert out.read_text(encoding="utf-8") == "# /// metadata\nimport requests"
    assert f.read_text(encoding="utf-8") == "import requests" # original unchanged
