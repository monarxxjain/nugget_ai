from sources.zomato_scraper import ZomatoScraper
from utils.logger import get_logger
import time

scrapers = [
    ZomatoScraper("https://www.zomato.com/lucknow/vint-club-ibb-sushant-golf-city"),
    ZomatoScraper(
        "https://www.zomato.com/lucknow/the-vibes-late-night-club-gomti-nagar"
    ),
    ZomatoScraper("https://www.zomato.com/lucknow/burger-king-hazratganj"),
    ZomatoScraper("https://www.zomato.com/lucknow/mcdonalds-hazratganj"),
    ZomatoScraper("https://www.zomato.com/lucknow/the-big-grill-gomti-nagar"),
]


def scrape_all():
    logger = get_logger()
    for scraper in scrapers:
        try:
            data = scraper.scrape()
            logger.info(f"[✓] Scraped: {data.restaurant_name}")

            with open(
                f"data/raw_json/{data.restaurant_name}.json", "w", encoding="utf-8"
            ) as f:
                f.write(data.model_dump_json(indent=2))
        except Exception as e:
            logger.error(f"[!] Failed scraping {scraper.base_url}: {e}")

        time.sleep(10)


if __name__ == "__main__":
    scrape_all()
