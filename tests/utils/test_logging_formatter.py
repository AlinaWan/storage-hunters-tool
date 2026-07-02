import logging
from datetime import datetime

from src.utils.logging_formatter import LoggingFormatter

def make_record(level=logging.INFO, created=1751382641.302, msg="Logger initialized and working."):
    record = logging.LogRecord(
        name="Bootstrap",
        level=level,
        pathname="test.py",
        lineno=1,
        msg=msg,
        args=(),
        exc_info=None
    )

    record.funcName = "main"
    record.created = created
    record.msecs = 302
    return record

def test_format_time_default():
    formatter = LoggingFormatter()
    record = make_record()

    expected = (
        datetime.fromtimestamp(record.created)
        .strftime("%Y-%m-%d %H:%M:%S")
        + f",{int(record.msecs):03d}"
    )

    assert formatter.formatTime(record) == expected

def test_format_time_custom_datefmt():
    formatter = LoggingFormatter()
    record = make_record()

    result = formatter.formatTime(
        record,
        "%Y/%m/%d"
    )

    assert result == "2025/07/01"

def test_format_replaces_level():
    formatter = LoggingFormatter()
    record = make_record(level=logging.INFO)

    result = formatter.format(record)

    assert "[INF]" in result

def test_format_restores_original_levelname():
    formatter = LoggingFormatter()
    record = make_record(level=logging.INFO)

    original = record.levelname

    formatter.format(record)

    assert record.levelname == original

def test_unknown_level_falls_back():
    formatter = LoggingFormatter()
    record = make_record(level=12345)

    result = formatter.format(record)

    assert "Level 12345" in result