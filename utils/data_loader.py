"""Data loader for Damyang retreat venues."""

import json
import math
from pathlib import Path
from typing import Optional

import pandas as pd


def load_venues() -> dict:
    """Load venues data from JSON file."""
    data_path = Path(__file__).parent.parent / "data" / "venues.json"
    with open(data_path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_venues_df() -> pd.DataFrame:
    """Get venues as a pandas DataFrame with computed coordinates."""
    data = load_venues()
    venues = data["venues"]
    areas = data["areas"]

    # Calculate coordinates based on area and name hash (matching original JS logic)
    for venue in venues:
        area_key = venue.get("area", "eup")
        area = areas.get(area_key, areas["eup"])

        # Hash-based coordinate offset (mimics original JS getCoords)
        name = venue["name"]
        hash_val = 0
        for char in name:
            hash_val = ord(char) + ((hash_val << 5) - hash_val)

        rand1 = (math.sin(hash_val) + 1) / 2
        rand2 = (math.cos(hash_val) + 1) / 2
        spread = 0.003

        venue["lat"] = area["lat"] + (rand1 - 0.5) * spread
        venue["lng"] = area["lng"] + (rand2 - 0.5) * spread
        venue["area_name"] = area["name"]

    return pd.DataFrame(venues)


def get_accommodation() -> dict:
    """Get accommodation details."""
    data = load_venues()
    return data["accommodation"]


def get_areas() -> dict:
    """Get area definitions."""
    data = load_venues()
    return data["areas"]


def calculate_distance(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """Calculate distance between two points in kilometers using Haversine formula."""
    R = 6371  # Earth's radius in km

    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lng = math.radians(lng2 - lng1)

    a = math.sin(delta_lat / 2) ** 2 + \
        math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lng / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c


def filter_venues(
    df: pd.DataFrame,
    categories: Optional[list] = None,
    areas: Optional[list] = None,
    max_distance_km: Optional[float] = None,
    search_query: Optional[str] = None
) -> pd.DataFrame:
    """Filter venues by various criteria."""
    filtered = df.copy()

    if categories:
        filtered = filtered[filtered["category"].isin(categories)]

    if areas:
        filtered = filtered[filtered["area_name"].isin(areas)]

    if max_distance_km is not None:
        accommodation = get_accommodation()
        acc_lat, acc_lng = accommodation["lat"], accommodation["lng"]

        distances = filtered.apply(
            lambda row: calculate_distance(acc_lat, acc_lng, row["lat"], row["lng"]),
            axis=1
        )
        filtered = filtered[distances <= max_distance_km]

    if search_query:
        query = search_query.lower()
        mask = (
            filtered["name"].str.lower().str.contains(query, na=False) |
            filtered["feature"].str.lower().str.contains(query, na=False) |
            filtered["address"].str.lower().str.contains(query, na=False)
        )
        filtered = filtered[mask]

    return filtered


# Category display info
CATEGORY_INFO = {
    "restaurant": {"emoji": "🍚", "label": "식당", "color": "#16a34a"},
    "cafe": {"emoji": "☕", "label": "카페", "color": "#f97316"},
    "activity": {"emoji": "🎨", "label": "Activity", "color": "#9333ea"},
}


def get_category_label(category: str) -> str:
    """Get display label for category."""
    info = CATEGORY_INFO.get(category, {})
    return f"{info.get('emoji', '')} {info.get('label', category)}"


def get_category_color(category: str) -> str:
    """Get color for category."""
    return CATEGORY_INFO.get(category, {}).get("color", "#6B7280")
