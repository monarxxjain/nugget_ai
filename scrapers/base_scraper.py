from abc import ABC, abstractmethod
from models.resturant import Restaurant


class BaseRestaurantScraper(ABC):
    def __init__(self, base_url: str):
        self.base_url = base_url

    @abstractmethod
    def scrape(self) -> Restaurant:
        """Main method to scrape and return structured Restaurant data"""
        pass
