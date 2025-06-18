import logging
from src.config_loader import load_config

def setup_logger(level=None):
    config = load_config()
    log_level_str = config.get("logging_level", "INFO").upper()

    # If a level argument is provided, override config level
    if level is not None:
        log_level_str = level.upper()

    log_level = getattr(logging, log_level_str, logging.INFO)

    logger = logging.getLogger("figure-caption-extractor")
    logger.setLevel(log_level)

    # Prevent adding multiple handlers if called multiple times
    if not logger.hasHandlers():
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(log_level)
        ch.setFormatter(formatter)
        logger.addHandler(ch)

        # Optional: File handler if you want to log to a file
        # fh = logging.FileHandler("figure-caption-extractor.log")
        # fh.setLevel(log_level)
        # fh.setFormatter(formatter)
        # logger.addHandler(fh)

    return logger

logger = setup_logger()
