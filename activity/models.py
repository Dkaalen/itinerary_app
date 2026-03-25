from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class Activity:
    source_sheet: str
    country: str
    destination: str
    destination_id: str | None
    slug: str
    title: str
    raw_text: str
    type: str | None = None
    price_eur_adult: float | None = None
    price_currency: str = "EUR"
    supplier: str | None = None
    supplier_url: str | None = None
    status: str | None = None
    comments: str | None = None
    booking_notes: dict[str, Any] = field(default_factory=dict)
    details: dict[str, str] = field(default_factory=dict)
    spreadsheet_row: int | None = None

    @property
    def label(self) -> str:
        if self.price_eur_adult is None:
            return self.title
        whole = int(self.price_eur_adult)
        price = whole if whole == self.price_eur_adult else self.price_eur_adult
        return f"{self.title} ({price}€ adult)"

    @property
    def short_description(self) -> str:
        includes = self.details.get("Includes")
        if includes:
            return includes
        notable = self.details.get("Notable sights")
        if notable:
            return notable
        return self.raw_text

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_sheet": self.source_sheet,
            "country": self.country,
            "destination": self.destination,
            "destination_id": self.destination_id,
            "slug": self.slug,
            "title": self.title,
            "raw_text": self.raw_text,
            "type": self.type,
            "price_eur_adult": self.price_eur_adult,
            "price_currency": self.price_currency,
            "supplier": self.supplier,
            "supplier_url": self.supplier_url,
            "status": self.status,
            "comments": self.comments,
            "booking_notes": self.booking_notes,
            "details": self.details,
            "spreadsheet_row": self.spreadsheet_row,
        }