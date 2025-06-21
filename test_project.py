import pytest
from pathlib import Path
from project import handleFile, process, watchFileChange, SUFFIX_MAP
import threading
import time
def test_process(monkeypatch, tmp_path):
    downloads_path = tmp_path / "Downloads"
    downloads_path.mkdir()
    monkeypatch.setattr(Path, "expanduser", lambda self: Path(str(self).replace("~", str(tmp_path))))
    for category, suffixes in SUFFIX_MAP.items():
        for suffix in suffixes:
            file = downloads_path / f"test{suffix}"
            file.write_bytes(b"test data")
            process(file, category)
            target = downloads_path / category / f"test{suffix}"
            assert target.exists()
            assert not file.exists()
            assert target.read_bytes() == b"test data"
    randomfile = downloads_path / "test.xyz"
    randomfile.write_bytes(b"random")
    process(randomfile,"etc")
    target = downloads_path / "etc" / "test.xyz"
    assert target.exists()
    assert not randomfile.exists()
    assert target.read_bytes() == b"random"

def test_handleFile(monkeypatch, tmp_path):
    downloads_path = tmp_path / "Downloads"
    downloads_path.mkdir()
    monkeypatch.setattr(Path, "expanduser", lambda self: Path(str(self).replace("~", str(tmp_path))))
    for category, suffixes in SUFFIX_MAP.items():
        for suffix in suffixes:
            file = downloads_path / f"test{suffix}"
            file.write_bytes(b"test data")
    randomfile = downloads_path / "test.xyz"
    randomfile.write_bytes(b"random")
    handleFile(downloads_path)
    for category, suffixes in SUFFIX_MAP.items():
        for suffix in suffixes:
            expect = downloads_path / category / f"test{suffix}"
            assert expect.exists()
            assert expect.read_bytes() == b"test data"
    expect = downloads_path / "etc" / "test.xyz"
    assert expect.exists()
    assert expect.read_bytes() == b"random"

def test_watchFileChange(monkeypatch, tmp_path):
    downloads_path = tmp_path / "Downloads"
    downloads_path.mkdir()
    monkeypatch.setattr(Path, "expanduser", lambda self: Path(str(self).replace("~", str(tmp_path))))

    thread = threading.Thread(target=watchFileChange, args=(downloads_path,), daemon=True)
    thread.start()

    time.sleep(1)

    for category, suffixes in SUFFIX_MAP.items():
        for suffix in suffixes:
            file_path = downloads_path / f"test{suffix}"
            file_path.write_bytes(b"test data")
            time.sleep(0.2) 

    time.sleep(2)

    for category, suffixes in SUFFIX_MAP.items():
        for suffix in suffixes:  
            expect = downloads_path / category / f"test{suffix}"
            assert expect.exists()
            assert expect.read_bytes() == b"test data"

    unknown_file = downloads_path / "unknown.xyz"
    unknown_file.write_text("data")
    time.sleep(0.5)
    assert (downloads_path / "etc" / "unknown.xyz").exists()

      

