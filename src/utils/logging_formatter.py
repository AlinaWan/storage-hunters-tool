import logging
import datetime
from typing import final as sealed, override

@sealed
class LoggingFormatter(logging.Formatter):
    LEVEL_MAP = {
        logging.DEBUG: "[DBG]",
        logging.INFO: "[INF]",
        logging.WARNING: "[WRN]",
        logging.ERROR: "[ERR]",
        logging.CRITICAL: "[CRT]"
    }

    def __init__(self):
        log_format = "%(asctime)s %(levelname)s %(name)s.%(funcName)s - %(message)s"
        super().__init__(fmt=log_format)

    @override
    def formatTime(self, record: logging.LogRecord, datefmt: str | None = None) -> str:
        if datefmt:
            return super().formatTime(record, datefmt)
        
        ct = datetime.datetime.fromtimestamp(record.created)
        return ct.strftime("%Y-%m-%d %H:%M:%S") + f",{int(record.msecs):03d}"

    @override
    def format(self, record: logging.LogRecord) -> str:
        original_levelname = record.levelname
        record.levelname = self.LEVEL_MAP.get(
            record.levelno,
            original_levelname
        )

        try:
            return super().format(record)
        finally:
            record.levelname = original_levelname