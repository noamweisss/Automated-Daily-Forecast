# Exploration & Test Scripts

This folder contains scripts created during the development and exploration phase of the project. These scripts helped us understand the XML structure and prove that data extraction works correctly.

## Working Scripts ✅

| Script | Purpose | Status |
|--------|---------|--------|
| `test_extraction_minimal.py` | Proves extraction works for one city (Tel Aviv) | Working |
| `extract_all_cities.py` | Extracts all 15 cities successfully, sorted north to south | Working |
| `inspect_xml.py` | Shows internal XML Element structure | Working |
| `test_date.py` | Tests Python date formatting | Working |
| `find_todays_forecast.py` | Lists all available dates in XML file | Working |

## Known Issues ⚠️

| Script | Issue |
|--------|-------|
| `parse_weather.py` | Unicode error - explores LocationData structure |

## Usage

These scripts are for reference and testing purposes. They helped validate our approach before building the production scripts.

### Examples

```bash
# Test minimal extraction (one city)
python exploration/test_extraction_minimal.py

# Test full extraction (all 15 cities)
python exploration/extract_all_cities.py

# See what dates are available in the XML
python exploration/find_todays_forecast.py

# Inspect XML structure
python exploration/inspect_xml.py
```

## Note

These scripts are kept for reference and troubleshooting. The production code will be in the root directory.
