import json
from pathlib import Path
from utils.logger import get_logger
from typing import Dict, Any
from pydantic import ValidationError
from models.resturant import Restaurant, Currency
from utils.exchange_rates import get_exchange_rates
from config.rag_config import RAW_JSON_DIR, PROCESSED_JSON_DIR

logger = get_logger()


def preprocess_json(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Preprocess the raw JSON data to conform to the Restaurant schema.
    Performs necessary transformations and validations.

    Args:
        data: Raw JSON data as a dictionary

    Returns:
        Processed dictionary conforming to the Restaurant schema
    """
    # Handle currency conversion if needed
    if "menu" in data:
        for section in data["menu"]:
            if "items" in section:
                for item in section["items"]:
                    if "currency" in item and isinstance(item["currency"], str):
                        item["currency"] = Currency.from_str(item["currency"])

    # Convert currency to INR using FX rates
    if "menu" in data:
        for section in data["menu"]:
            if "items" in section:
                for item in section["items"]:
                    if item["currency"] != Currency.INR:
                        currency = item["currency"]

                        # Get current exchange rates
                        rates = get_exchange_rates()
                        conversion_rate = rates.get(currency)
                        if conversion_rate is None:
                            if currency == Currency.OTHER:
                                continue
                            # Default fallback rate
                            conversion_rate = 1.0
                        item["price"] *= conversion_rate
                        item["currency"] = Currency.INR

    return data


def process_file(input_file: Path) -> bool:
    try:
        output_file = PROCESSED_JSON_DIR / input_file.name

        logger.info(f"Processing file: {input_file}")
        with open(input_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        processed_data = preprocess_json(data)

        restaurant = Restaurant.model_validate(processed_data)

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(restaurant.model_dump_json(indent=2))

        logger.info(f"Successfully processed: {input_file} -> {output_file}")
        return True

    except json.JSONDecodeError:
        logger.error(f"Invalid JSON in file: {input_file}")
    except ValidationError as e:
        logger.error(f"Validation error in {input_file}: {e}")
    except Exception as e:
        logger.error(f"Error processing {input_file}: {str(e)}")

    return False


def main():
    RAW_JSON_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_JSON_DIR.mkdir(parents=True, exist_ok=True)

    json_files = list(RAW_JSON_DIR.glob("*.json"))

    # remove sample.json if exists
    json_files = [f for f in json_files if f.name != "sample.json"]

    if not json_files:
        logger.warning(f"No JSON files found in {RAW_JSON_DIR}")
        return

    logger.info(f"Found {len(json_files)} JSON files to process")

    success_count = 0
    for json_file in json_files:
        if process_file(json_file):
            success_count += 1

    logger.info(
        f"Processing complete. {success_count}/{len(json_files)} files successfully processed."
    )


if __name__ == "__main__":
    main()
