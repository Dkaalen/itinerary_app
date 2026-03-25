from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

from .models import Activity


_DATA_PATH = Path(__file__).with_name("data.json")


def _load_raw_data() -> list[dict]:
    with _DATA_PATH.open("r", encoding="utf-8") as f:
        payload = json.load(f)
    return payload["activities"]


def load_activities() -> list[Activity]:
    return [Activity(**item) for item in _load_raw_data()]


ACTIVITIES: list[Activity] = load_activities()

ACTIVITIES_BY_DESTINATION: dict[str, list[Activity]] = defaultdict(list)
for activity in ACTIVITIES:
    ACTIVITIES_BY_DESTINATION[activity.destination].append(activity)

DESTINATIONS: list[str] = sorted(ACTIVITIES_BY_DESTINATION)


def get_activities(destination: str) -> list[Activity]:
    return list(ACTIVITIES_BY_DESTINATION.get(destination, []))


def find_activity(destination: str, slug: str) -> Activity | None:
    for activity in ACTIVITIES_BY_DESTINATION.get(destination, []):
        if activity.slug == slug:
            return activity
    return None


def destination_options(destination: str) -> list[str]:
    return [activity.label for activity in get_activities(destination)]


def as_streamlit_options(destination: str) -> list[dict]:
    return [activity.to_dict() for activity in get_activities(destination)]