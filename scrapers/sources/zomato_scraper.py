import requests
import requests_cache
from models.resturant import (
    MenuItem,
    MenuSection,
    Restaurant,
    Location,
    Contact,
    Currency,
    Review,
)
from scrapers.base_scraper import BaseRestaurantScraper
from utils.logger import get_logger

logger = get_logger()

requests_cache.install_cache("my_cache", expire_after=3000)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.zomato.com/",
    "DNT": "1",
    "Connection": "keep-alive",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
}


class ZomatoScraper(BaseRestaurantScraper):
    """
    A scraper specifically designed for Zomato restaurant pages,
    based on the HTML structure observed around April 2025.
    """

    def __init__(self, restaurant_url: str):
        """
        Initializes the Zomato scraper for a specific restaurant URL.

        Args:
            restaurant_url: The full URL of the Zomato restaurant page to scrape.
        """
        super().__init__(
            restaurant_url.rstrip("/")
        )  # For this specific scraper, base_url is the restaurant URL
        self.source_url = "https://www.zomato.com/webroutes/getPage?page_url="

    def _get_menu(self) -> list[MenuSection]:
        menu_items_page_url = f"{self.source_url}{self.base_url}/order"
        logger.info(f"[+] Scraping Zomato restaurant page: {menu_items_page_url}")

        try:
            response = requests.get(menu_items_page_url, headers=headers, timeout=30)
            response.raise_for_status()  # Raise exception for 4XX/5XX responses
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch restaurant page: {e}")
            raise RuntimeError(f"Failed to fetch restaurant data: {e}")

        try:
            response_data = response.json()
            menu_sections = (
                response_data.get("page_data", {})
                .get("order", {})
                .get("menuList", {})
                .get("menus", [])
            )
        except (ValueError, KeyError) as e:
            logger.error(f"Failed to parse JSON response: {e}")
            raise ValueError(f"Failed to parse restaurant data: {e}")

        menu_store = []

        for menu_section in menu_sections:
            menu = menu_section.get("menu", {})
            section_name = menu.get("name", "Unnamed Section")
            categories = menu.get("categories", [])
            for category in categories:
                category = category.get("category", {})
                category_name = category.get("name", "Unnamed Category")
                menu_items = []
                items = category.get("items", [])
                for item in items:
                    try:
                        item = item.get("item", {})
                        item_name = item.get("name", "Unnamed Item")
                        description = item.get("desc", "")
                        price = item.get("display_price", 0)
                        if price == 0 or price == "0":
                            price = item.get("price", 0)
                        currency = Currency.INR
                        tags = item.get("tag_slugs", [])
                        menu_items.append(
                            MenuItem(
                                item_name=item_name,
                                description=description,
                                price=price,
                                currency=currency,
                                tags=tags,
                            )
                        )
                    except Exception as e:
                        logger.error(f"Error processing menu item: {e}")
                        continue

                menu_section = MenuSection(
                    section=f"{section_name} {category_name}".strip(), items=menu_items
                )
                menu_store.append(menu_section)

        return menu_store

    def _get_location(self) -> Location:
        menu_items_page_url = f"{self.source_url}{self.base_url}/order"
        logger.info(f"[+] Scraping Zomato restaurant page: {menu_items_page_url}")

        try:
            response = requests.get(menu_items_page_url, headers=headers, timeout=30)
            response.raise_for_status()  # Raise exception for 4XX/5XX responses
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch restaurant page: {e}")
            raise RuntimeError(f"Failed to fetch restaurant data: {e}")

        try:
            response_data = response.json()
            location = response_data.get("location", {})
            address = (
                response_data.get("page_data", {})
                .get("sections", {})
                .get("SECTION_RES_CONTACT", {})
                .get("address", {})
            )
        except (ValueError, KeyError) as e:
            logger.error(f"Failed to parse JSON response: {e}")
            raise ValueError(f"Failed to parse restaurant data: {e}")
        return Location(
            address=address,
            city=location.get("cityName"),
            pincode=None,
            latitude=location.get("latitude"),
            longitude=location.get("longitude"),
        )

    def _get_name(self) -> str:
        menu_items_page_url = f"{self.source_url}{self.base_url}/order"
        logger.info(f"[+] Scraping Zomato restaurant page: {menu_items_page_url}")

        try:
            response = requests.get(menu_items_page_url, headers=headers, timeout=30)
            response.raise_for_status()  # Raise exception for 4XX/5XX responses
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch restaurant page: {e}")
            raise RuntimeError(f"Failed to fetch restaurant data: {e}")

        try:
            response_data = response.json()
            name = (
                response_data.get("page_data", {})
                .get("sections", {})
                .get("SECTION_BASIC_INFO", {})
                .get("name", "No Name Found")
            )
        except (ValueError, KeyError) as e:
            logger.error(f"Failed to parse JSON response: {e}")
            raise ValueError(f"Failed to parse restaurant data: {e}")

        return name

    def _get_reviews(self) -> list[Review]:
        reviews_page_url = f"{self.source_url}{self.base_url}/reviews"
        logger.info(f"[+] Scraping Zomato restaurant page: {reviews_page_url}")

        try:
            response = requests.get(reviews_page_url, headers=headers, timeout=30)
            response.raise_for_status()  # Raise exception for 4XX/5XX responses
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch restaurant page: {e}")
            raise RuntimeError(f"Failed to fetch restaurant data: {e}")

        try:
            response_data = response.json()
            reviews = response_data.get("entities", {}).get("REVIEWS", {})
        except (ValueError, KeyError) as e:
            logger.error(f"Failed to parse JSON response: {e}")
            raise ValueError(f"Failed to parse restaurant data: {e}")

        reviews_store = []

        for review in reviews.values():
            review_text = review.get("reviewText", "")
            rating = review.get("ratingV2", 0)

            reviews_store.append(
                Review(
                    rating=rating,
                    review_text=review_text,
                )
            )
        return reviews_store

    def _get_features(self) -> list[str]:
        page_url = f"{self.source_url}{self.base_url}"
        logger.info(f"[+] Scraping Zomato restaurant page: {page_url}")

        try:
            response = requests.get(page_url, headers=headers, timeout=30)
            response.raise_for_status()  # Raise exception for 4XX/5XX responses
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch restaurant page: {e}")
            raise RuntimeError(f"Failed to fetch restaurant data: {e}")

        try:
            response_data = response.json()
            cost_for_two = (
                response_data.get("page_data", {})
                .get("sections", {})
                .get("SECTION_RES_DETAILS", {})
                .get("CFT_DETAILS", {})
                .get("cfts", [])
            )

            highlights = (
                response_data.get("page_data", {})
                .get("sections", {})
                .get("SECTION_RES_DETAILS", {})
                .get("HIGHLIGHTS", {})
                .get("highlights", [])
            )

            cuisines = (
                response_data.get("page_data", {})
                .get("sections", {})
                .get("SECTION_RES_DETAILS", {})
                .get("CUISINES", {})
                .get("cuisines", [])
            )

            top_dishes = (
                response_data.get("page_data", {})
                .get("sections", {})
                .get("SECTION_RES_DETAILS", {})
                .get("TOP_DISHES", {})
            )

            people_liked = (
                response_data.get("page_data", {})
                .get("sections", {})
                .get("SECTION_REVIEW_HIGHLIGHTS", {})
                .get("PEOPLE_LIKED", {})
            )

        except (ValueError, KeyError) as e:
            logger.error(f"Failed to parse JSON response: {e}")
            raise ValueError(f"Failed to parse restaurant data: {e}")

        features_store = []

        for cost in cost_for_two:
            cost_title = cost.get("title", "")
            cost_subtitle = cost.get("subtitle", "")
            if cost_title:
                features_store.append(f"Cost for Two: {cost_title} {cost_subtitle}")

        for highlight in highlights:
            highlight_title = highlight.get("text", "")
            if highlight_title:
                features_store.append(f"Highlight: {highlight_title}")

        for cuisine in cuisines:
            cuisine_title = cuisine.get("name", "")
            if cuisine_title:
                features_store.append(f"Cuisine: {cuisine_title}")

        if top_dishes:
            features_store.append(
                f"{top_dishes.get('title', '')} {top_dishes.get('description', '')}"
            )

        if people_liked:
            people_liked_title = people_liked.get("title", "")
            people_liked_description = people_liked.get("description", "")
            if people_liked_title:
                features_store.append(
                    f"{people_liked_title} {people_liked_description}"
                )

        return features_store

    def _get_description(self) -> str:
        page_url = f"{self.source_url}{self.base_url}"
        logger.info(f"[+] Scraping Zomato restaurant page: {page_url}")

        try:
            response = requests.get(page_url, headers=headers, timeout=30)
            response.raise_for_status()  # Raise exception for 4XX/5XX responses
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch restaurant page: {e}")
            raise RuntimeError(f"Failed to fetch restaurant data: {e}")

        try:
            response_data = response.json()
            description = (
                response_data.get("page_data", {})
                .get("sections", {})
                .get("SECTION_BASIC_INFO", {})
                .get("cuisine_string", "")
            )
        except (ValueError, KeyError) as e:
            logger.error(f"Failed to parse JSON response: {e}")
            raise ValueError(f"Failed to parse restaurant data: {e}")

        return description

    def _get_contact(self) -> Contact:
        menu_items_page_url = f"{self.source_url}{self.base_url}/order"
        logger.info(f"[+] Scraping Zomato restaurant page: {menu_items_page_url}")

        try:
            response = requests.get(menu_items_page_url, headers=headers, timeout=30)
            response.raise_for_status()  # Raise exception for 4XX/5XX responses
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch restaurant page: {e}")
            raise RuntimeError(f"Failed to fetch restaurant data: {e}")

        try:
            response_data = response.json()
            phone_details = (
                response_data.get("page_data", {})
                .get("sections", {})
                .get("SECTION_RES_CONTACT", {})
                .get("phoneDetails", {})
            )
        except (ValueError, KeyError) as e:
            logger.error(f"Failed to parse JSON response: {e}")
            raise ValueError(f"Failed to parse restaurant data: {e}")

        if phone_details:
            phone = phone_details.get("phoneStr", None)

            return Contact(phone=phone, email=None, website=None)

        return Contact(phone=None, email=None, website=None)

    def _get_operating_hours(self) -> dict:
        menu_items_page_url = f"{self.source_url}{self.base_url}/order"
        logger.info(f"[+] Scraping Zomato restaurant page: {menu_items_page_url}")

        try:
            response = requests.get(menu_items_page_url, headers=headers, timeout=30)
            response.raise_for_status()  # Raise exception for 4XX/5XX responses
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch restaurant page: {e}")
            raise RuntimeError(f"Failed to fetch restaurant data: {e}")

        try:
            response_data = response.json()
            operating_hours = (
                response_data.get("page_data", {})
                .get("sections", {})
                .get("SECTION_BASIC_INFO", {})
                .get("timing", {})
                .get("customised_timings", {})
                .get("opening_hours", [])
            )
        except (ValueError, KeyError) as e:
            logger.error(f"Failed to parse JSON response: {e}")
            raise ValueError(f"Failed to parse restaurant data: {e}")

        operating_hours_store = dict()
        for day in operating_hours:
            timing = day.get("timing", "")
            days = day.get("days", "")
            if timing and days:
                operating_hours_store[days] = timing

        return operating_hours_store

    def scrape(self) -> Restaurant:
        menu_store = self._get_menu()
        location = self._get_location()
        resturant_name = self._get_name()
        reviews = self._get_reviews()
        contact = self._get_contact()
        operating_hours = self._get_operating_hours()
        features = self._get_features()
        description = self._get_description()

        return Restaurant(
            restaurant_name=resturant_name,
            description=description,
            location=location,
            contact=contact,
            operating_hours=operating_hours,
            features=features,
            menu=menu_store,
            reviews=reviews,
        )
