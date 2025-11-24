# Title Owner Lookup - Module Documentation

## Overview

The title owner lookup module extends the county data extraction system to scrape property owner information from Fulton County and DeKalb County property search websites.

## Architecture

### New Modules

```
title_scraper.py          # Web scraping for title owner lookup
title_processor.py        # Extended data processor with owner lookup
main_with_owners.py       # Entry point for complete processing
test_title_scraper.py     # Test script for verification
```

### Module Flow

```
main_with_owners.py
    ↓
┌───────────────────────────────────┐
│  Step 1: Geocode Counties         │
│  (uses existing modules)           │
│  • config.py                       │
│  • geocoder.py                     │
│  • data_processor.py               │
└─────────────┬─────────────────────┘
              ↓
┌───────────────────────────────────┐
│  Step 2: Lookup Title Owners      │
│  (new modules)                     │
│  • title_scraper.py                │
│  • title_processor.py              │
└─────────────┬─────────────────────┘
              ↓
         Output CSV
```

## Classes

### TitleOwnerLookup (title_scraper.py)

Web scraper for county property search websites.

**Methods:**
- `lookup_fulton_county(street, city)` - Scrape Fulton County
- `lookup_dekalb_county(street, city)` - Scrape DeKalb County
- `lookup_owner(street, city, county)` - Auto-detect county and scrape
- `close()` - Clean up resources

**Features:**
- Selenium WebDriver automation
- BeautifulSoup HTML parsing
- Headless browser support
- Error handling and logging
- Context manager support

**Example:**
```python
from config import Config
from title_scraper import TitleOwnerLookup

config = Config()
with TitleOwnerLookup(config.fulton_county_url, config.dekalb_county_url) as scraper:
    owner = scraper.lookup_owner("123 Main St", "Atlanta", "Fulton County")
    print(owner)
```

### TitleOwnerProcessor (title_processor.py)

Extended data processor that combines geocoding and title lookup.

**Methods:**
- `identify_missing_owners(df)` - Find rows needing owner lookup
- `process_title_owner(idx, row, df, progress, total)` - Lookup single owner
- `process_title_owners(df)` - Process all missing owners
- `process_csv_with_owners(input, output)` - Complete pipeline

**Inherits from:** `CountyDataProcessor`

**Example:**
```python
from geocoder import CensusGeocoder
from title_scraper import TitleOwnerLookup
from title_processor import TitleOwnerProcessor

geocoder = CensusGeocoder(census_url)
with TitleOwnerLookup(fulton_url, dekalb_url) as scraper:
    processor = TitleOwnerProcessor(geocoder, scraper)
    processor.process_csv_with_owners("input.csv", "output.csv")
```

## Usage

### Basic Usage

```bash
# Run complete processing (geocoding + title lookup)
uv run python main_with_owners.py
```

### Test First

```bash
# Test with sample addresses (opens browser to watch)
uv run python test_title_scraper.py
```

### Step-by-Step

```python
from config import Config
from geocoder import CensusGeocoder
from title_scraper import TitleOwnerLookup
from title_processor import TitleOwnerProcessor

# 1. Load configuration
config = Config()

# 2. Initialize components
geocoder = CensusGeocoder(config.get_census_url())

# 3. Create scraper (use context manager for cleanup)
with TitleOwnerLookup(
    fulton_url=config.fulton_county_url,
    dekalb_url=config.dekalb_county_url,
    headless=True  # Set False to see browser
) as scraper:
    
    # 4. Create processor
    processor = TitleOwnerProcessor(geocoder, scraper)
    
    # 5. Process CSV
    processor.process_csv_with_owners(
        "Data/input.csv",
        "Data/output.csv"
    )
```

## Configuration

Add to `.env` file:

```env
# Required for title lookup
FULTON_COUNTY_URL="https://qpublic.schneidercorp.com/Application.aspx?App=FultonCountyGA&PageType=Search"
DEALB_COUNTY_URL="https://qpublic.schneidercorp.com/Application.aspx?AppID=994&PageTypeID=2&pageID=8822"
```

## Dependencies

New dependencies added:

```toml
selenium>=4.16.0           # Browser automation
beautifulsoup4>=4.12.0     # HTML parsing
webdriver-manager>=4.0.0   # Automatic Chrome driver management
```

## How It Works

### 1. Web Scraping Process

```
1. Initialize Chrome WebDriver (headless mode)
   ↓
2. Navigate to county property search page
   ↓
3. Find and fill address search field
   ↓
4. Click search button
   ↓
5. Wait for results page
   ↓
6. Click first matching property link
   ↓
7. Parse property details page with BeautifulSoup
   ↓
8. Extract owner name from HTML
   ↓
9. Return owner name or None
```

### 2. Data Processing Pipeline

```
Input CSV
   ↓
Load DataFrame
   ↓
┌────────────────────────────────┐
│ Step 1: Geocode Counties       │
│ • Identify missing counties     │
│ • Call Census API               │
│ • Fill in county names          │
└────────────┬───────────────────┘
             ↓
┌────────────────────────────────┐
│ Step 2: Lookup Title Owners    │
│ • Identify missing owners       │
│ • Scrape county websites        │
│ • Fill in owner names           │
└────────────┬───────────────────┘
             ↓
Save Updated CSV
```

## Features

✓ **Automatic County Detection**
  - Reads county from DataFrame
  - Routes to correct county website
  - Handles Fulton and DeKalb counties

✓ **Robust Web Scraping**
  - Selenium for dynamic pages
  - BeautifulSoup for HTML parsing
  - Multiple fallback patterns for finding owner data
  - Error handling for missing elements

✓ **Headless Mode**
  - Run without visible browser (default)
  - Option to show browser for debugging
  - Faster processing in headless mode

✓ **Logging**
  - Detailed logs saved to `title_lookup.log`
  - Console output for progress
  - Error tracking and debugging

✓ **Resource Management**
  - Context manager for cleanup
  - Automatic browser closure
  - Memory efficient

## Error Handling

### Common Issues

**1. Element Not Found**
- Multiple fallback patterns for finding form fields
- Logs warning and returns None
- Processing continues with next address

**2. No Search Results**
- Returns None if no properties match
- Logs warning with address details
- Processing continues

**3. Page Timeout**
- 10-second timeout for page loads
- Returns None on timeout
- Logs timeout error

**4. Network Issues**
- Catches connection errors
- Logs error details
- Returns None for failed lookups

## Performance

### Speed Considerations

- **Selenium overhead:** ~2-5 seconds per property
- **For 127 properties:** ~5-10 minutes
- **Network dependent:** Varies with site speed
- **Parallel processing:** Not recommended (may get rate-limited)

### Optimization Tips

1. **Process in batches:** Run overnight for large datasets
2. **Cache results:** Store in database to avoid re-scraping
3. **Check first:** Only scrape properties missing owner data
4. **Headless mode:** Faster than visible browser

## Output

### CSV Columns Updated

- **CountyName:** Filled by geocoding (if missing)
- **Title Owner:** Filled by web scraping (if missing)

### Example Output

```csv
StreetAddress,City,State,CountyName,Title Owner
"220 Semel Cir NW","Atlanta","GA","Fulton County","JOHN DOE"
"2651 Avon Cv","Atlanta","GA","DeKalb County","JANE SMITH LLC"
```

## Troubleshooting

### Issue: "ChromeDriver not found"
**Solution:** webdriver-manager downloads it automatically on first run

### Issue: "Element not found" errors
**Solution:** 
- Website structure may have changed
- Update element IDs in `title_scraper.py`
- Use browser inspection tools to find new selectors

### Issue: Scraper returns None for valid addresses
**Solution:**
- Test with `headless=False` to see what's happening
- Check if address format matches county site expectations
- Verify county website is accessible

### Issue: Slow performance
**Solution:**
- Use headless mode (default)
- Process only missing owners
- Consider running during off-peak hours

## Testing

### Quick Test (3 addresses)

```bash
uv run python test_title_scraper.py
```

This tests:
1. Fulton County lookup
2. DeKalb County lookup  
3. Auto-detection by county name

### Full Processing Test

```bash
# Process first 10 rows only (modify script)
uv run python main_with_owners.py
```

## Extending the Scraper

### Add New County

```python
def lookup_new_county(self, street_address: str, city: str) -> Optional[str]:
    """Look up title owner for New County."""
    try:
        self._init_driver()
        self.driver.get(self.new_county_url)
        
        # Find search fields (inspect website)
        address_field = self.driver.find_element(By.ID, "address_field_id")
        address_field.send_keys(street_address)
        
        # Submit and parse results
        # ... (similar pattern to existing methods)
        
        return owner_name
    except Exception as e:
        self.logger.error(f"Error: {e}")
        return None
```

### Add Caching

```python
class CachedTitleLookup(TitleOwnerLookup):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cache = {}
    
    def lookup_owner(self, street, city, county):
        key = f"{street}|{city}|{county}"
        if key not in self.cache:
            self.cache[key] = super().lookup_owner(street, city, county)
        return self.cache[key]
```

## Best Practices

1. **Test first** with a few addresses before processing full dataset
2. **Use headless mode** for production runs
3. **Monitor logs** for errors and issues
4. **Backup data** before processing
5. **Run during off-hours** to minimize site impact
6. **Handle failures gracefully** - not all lookups will succeed
7. **Cache results** if re-processing same data

## Limitations

- Only supports Fulton and DeKalb counties currently
- Requires stable internet connection
- Dependent on county website structure (may break if sites change)
- Rate limiting by county websites possible
- Not suitable for real-time lookups (use API if available)
- Chrome browser required (via Selenium)

## Future Enhancements

- [ ] Add more Georgia counties
- [ ] Implement retry logic for failed lookups
- [ ] Add parallel processing with rate limiting
- [ ] Cache results in database
- [ ] API integration if counties provide APIs
- [ ] Better progress indicators (progress bar)
- [ ] Export logs to CSV for analysis
- [ ] Add proxy support for rate limit avoidance

## License

See LICENSE file for details.
