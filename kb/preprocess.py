import json
from langchain_core.documents import Document
from typing import List
from config.rag_config import PROCESSED_JSON_DIR
from models.resturant import Restaurant
from utils.logger import get_logger


logger = get_logger()


def extract_docs() -> List[Document]:
    docs = []

    for file_path in PROCESSED_JSON_DIR.glob("*.json"):
        with open(file_path, "r", encoding="utf-8") as f:
            raw_data = json.load(f)

        try:
            restaurant = Restaurant(**raw_data)
        except Exception as e:
            logger.warning(f"[!] Skipping {file_path.name}: {e}")
            continue

        for section in restaurant.menu:
            batch_size = 10
            for i in range(0, len(section.items), batch_size):
                batch_items = section.items[i : i + batch_size]
                batch_content = f"""
                Restaurant: {restaurant.restaurant_name}
                Description: {restaurant.description or "N/A"}
                Location: {restaurant.location.address}, {restaurant.location.city}
                Section: {section.section}
                Features: {", ".join(restaurant.features)}
                Items:
                """

                for item in batch_items:
                    batch_content += f"""
                    - {item.item_name} ({item.price} {item.currency})
                      Tags: {", ".join(item.tags)}
                      Description: {item.description or "N/A"}
                    """

                batch_content += "\nReviews:"
                for review in restaurant.reviews:
                    batch_content += f"""
                    - {review.rating} stars
                      Review: {review.review_text or "N/A"}\n
                    """

                docs.append(
                    Document(
                        page_content=batch_content.strip(),
                        metadata={"restaurant": restaurant.restaurant_name},
                    )
                )

    return docs
