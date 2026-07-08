"""Domain entities independent of database/API frameworks."""
from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass(frozen=True)
class MarketObservation:
    date: str
    source: str
    category: str
    item: str
    region: str = "Indonesia"
    price: Optional[float] = None
    volume: Optional[float] = None
    metric: str = "price"
    currency: str = "IDR"

@dataclass(frozen=True)
class SourceConfig:
    name: str
    url: str
    source_type: str = "html_table"
    table_index: int = 0
    notes: str = ""
    active: bool = True

@dataclass(frozen=True)
class AlertEvent:
    severity: str
    type: str
    item: str
    message: str
    region: str | None = None
    value: float | None = None
