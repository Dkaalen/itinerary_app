# activity package

This folder is ready to drop into your app as an `activity` module.

## What is inside
- `data.json` — parsed activity catalog from **Cheat Sheet 2.0.xlsx**
- `models.py` — `Activity` dataclass
- `catalog.py` — helper functions for loading and filtering activities
- `build_from_workbook.py` — rebuilds `data.json` from a newer workbook export

## Current catalog size
- Activities: 162
- Destinations: 17

## Quick use

```python
from activity import get_activities, destination_options

oslo_activities = get_activities("Oslo")
labels = destination_options("Oslo")
```

## Streamlit example

```python
import streamlit as st
from activity import get_activities

destination = "Oslo"
options = get_activities(destination)

selected = st.selectbox(
    "Choose activity",
    options,
    format_func=lambda activity: activity.label,
)

st.write(selected.short_description)
st.write(f"Price: {selected.price_eur_adult}€ adult")
```

## Notes
- Prices are read from the spreadsheet `Sales P per unit` column.
- The parser keeps the original raw text in `raw_text`.
- Parsed fields such as `Time`, `Meeting point`, `Includes`, and `Notable sights` are stored in `details`.
- For a few Iceland rows, the spreadsheet `ID` is abbreviated. The package uses the destination prefix from the activity text when available, such as `Reykjavik`.