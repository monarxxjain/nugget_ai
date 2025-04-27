from pydantic import BaseModel, Field, HttpUrl, EmailStr
from typing import List, Optional, Dict
from enum import Enum


class Currency(str, Enum):
    INR = "INR"
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"
    OTHER = "OTHER"

    @staticmethod
    def from_str(label: str):
        try:
            return Currency(label)
        except ValueError:
            return Currency.OTHER


class MenuItem(BaseModel):
    item_name: str
    description: Optional[str]
    price: float
    currency: Currency = Currency.INR
    tags: List[str] = Field(default_factory=list)


class MenuSection(BaseModel):
    section: str
    items: List[MenuItem]


class Location(BaseModel):
    address: str
    city: str
    pincode: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]


class Contact(BaseModel):
    phone: Optional[str]
    email: Optional[EmailStr]
    website: Optional[HttpUrl]


class Review(BaseModel):
    rating: float
    review_text: str


class Restaurant(BaseModel):
    restaurant_name: str
    description: Optional[str]
    location: Location
    contact: Optional[Contact]
    operating_hours: Dict[str, str]
    features: List[str] = Field(
        default_factory=list
    )  # vegetarian options, spice levels, allergen information
    menu: List[MenuSection]
    reviews: List[Review]
