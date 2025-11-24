# Title Owner Lookup - Quick Start Guide

## Installation

```bash
# Install dependencies
uv sync
```

## Quick Commands

### Test Scraper (Recommended First)
```bash
# Test with 3 sample addresses
uv run python test_title_scraper.py
```

### Full Processing
```bash
# Geocode counties + lookup owners
uv run python main_with_owners.py
```

### County Geocoding Only
```bash
# Just geocode (no title lookup)
uv run python main.py
```

## Simple Example

```python
from config import Config
from title_scraper import TitleOwnerLookup

config = Config()

# Lookup single owner
with TitleOwnerLookup(config.fulton_county_url, config.dekalb_county_url) as scraper:
    owner = scraper.lookup_owner(
        street_address="220 Semel Cir NW",
        city="Atlanta",
        county="Fulton County"
    )
    print(f"Owner: {owner}")
```

## Configuration Required

Add to `.env`:

```env
FULTON_COUNTY_URL="https://qpublic.schneidercorp.com/Application.aspx?App=FultonCountyGA&PageType=Search"
DEALB_COUNTY_URL="https://qpublic.schneidercorp.com/Application.aspx?AppID=994&PageTypeID=2&pageID=8822"
```

## Process Flow

```
1. Load CSV
2. Geocode counties (Census API)
3. Lookup owners (Web scraping)
4. Save updated CSV
```

## What Gets Updated

- **CountyName** column (if missing)
- **Title Owner** column (if missing)

## Expected Time

- **127 properties:** ~5-10 minutes
- **Larger datasets:** Plan for overnight processing

## Output Files

- **CSV:** `Data/...with_owners.csv`
- **Log:** `title_lookup.log`

## Quick Debugging

Set `headless=False` to watch the browser:

```python
with TitleOwnerLookup(..., headless=False) as scraper:
    # Now you can see what's happening
    owner = scraper.lookup_fulton_county("123 Main St", "Atlanta")
```

## Common Issues

| Issue | Solution |
|-------|----------|
| Chrome not found | webdriver-manager installs automatically |
| Element not found | Website changed - update selectors |
| Returns None | Test with headless=False to debug |
| Slow performance | Use headless=True (default) |

## Success Indicators

✓ Chrome driver installed automatically
✓ Browser opens (if not headless)
✓ County websites load
✓ Owner names extracted
✓ CSV updated with results

## When to Use Each Script

- **test_title_scraper.py** - Test 3 addresses quickly
- **main.py** - Only geocode counties
- **main_with_owners.py** - Full pipeline (recommended)

## Best Practices

1. ✓ Test first with small sample
2. ✓ Use headless mode for production
3. ✓ Monitor logs for errors
4. ✓ Backup data before processing
5. ✓ Run during off-peak hours

## File Structure

```
title-db-georgia/
├── title_scraper.py       # Web scraping module
├── title_processor.py     # Extended processor
├── main_with_owners.py    # Full pipeline
├── test_title_scraper.py  # Test script
└── title_lookup.log       # Generated logs
```

## Module Imports

```python
# Web scraping
from title_scraper import TitleOwnerLookup

# Extended processing
from title_processor import TitleOwnerProcessor

# Configuration
from config import Config
```

## Supported Counties

- ✓ Fulton County
- ✓ DeKalb County
- ✗ Others (coming soon)

## Dependencies Added

```
selenium>=4.16.0
beautifulsoup4>=4.12.0
webdriver-manager>=4.0.0
```

## Troubleshooting Commands

```bash
# Check dependencies
uv run python -c "import selenium; print('OK')"

# Test config
uv run python -c "from config import Config; c=Config(); print('OK')"

# View logs
cat title_lookup.log  # Linux/Mac
type title_lookup.log  # Windows
```

## Performance Tips

- Use headless mode (default)
- Process only missing data
- Cache results if re-processing
- Consider parallel processing for large datasets

## Next Steps

1. Run test script
2. Verify results
3. Run full processing
4. Check output CSV
5. Review logs for any issues

For detailed documentation, see `docs/TITLE_OWNER_LOOKUP.md`
