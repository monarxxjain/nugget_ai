import logging


def get_logger(name="zomato_scraper"):
    logger = logging.getLogger(name)

    # Check if the logger is already configured
    if not logger.hasHandlers():
        logger.setLevel(logging.INFO)

        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        ch.setFormatter(formatter)

        logger.addHandler(ch)

    return logger
