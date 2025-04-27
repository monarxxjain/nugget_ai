from functools import lru_cache
import requests

from models.resturant import Currency
from utils.logger import get_logger

logger = get_logger()


@lru_cache(maxsize=1, typed=True)
def get_exchange_rates():
    """Fetch current exchange rates from a public API and cache the result."""
    try:
        response = requests.get("https://api.exchangerate-api.com/v4/latest/INR")
        data = response.json()
        # Convert to INR-based rates (INR as base currency)
        rates = {
            Currency.USD: 1 / data["rates"]["USD"],
            Currency.EUR: 1 / data["rates"]["EUR"],
            Currency.GBP: 1 / data["rates"]["GBP"],
        }
        return rates
    except Exception as e:
        logger.error(f"Failed to fetch exchange rates: {e}")
        # Fallback rates if API fails
        return {Currency.USD: 85.34, Currency.EUR: 97.2, Currency.GBP: 113.58}
