# Quick Reference Guide

## File Structure

```
title-db-georgia/
├── config.py           # Configuration management
├── geocoder.py         # Census API geocoding
├── data_processor.py   # CSV processing engine
├── utils.py            # Analysis and utilities
├── examples.py         # Usage examples
├── main.py            # Main application
└── docs/
    └── ARCHITECTURE.md # Detailed architecture docs
```

## Quick Commands

### Run Main Application
```bash
uv run main.py
```

### Analyze Data
```bash
# Analyze a CSV file
uv run python utils.py "Data/filename.csv"

# Compare original vs updated
uv run python utils.py compare "Data/original.csv" "Data/updated.csv"
```

### Run Examples
```bash
uv run python examples.py
```

## Module Import Guide

### Import Configuration
```python
from config import Config

config = Config()
census_url = config.get_census_url()
```

### Import Geocoder
```python
from geocoder import CensusGeocoder

geocoder = CensusGeocoder(api_url="...", delay=0.5)
county = geocoder.geocode_address("street", "city", "state", "zip")
```

### Import Data Processor
```python
from data_processor import CountyDataProcessor

processor = CountyDataProcessor(geocoder)
processor.process_csv_file("input.csv", "output.csv")
```

### Import Utilities
```python
from utils import DataAnalyzer, DataCleaner

# Analyze
analysis = DataAnalyzer.analyze_csv("file.csv")

# Generate report
DataAnalyzer.generate_report("file.csv")

# Clean data
cleaned_df = DataCleaner.normalize_addresses(df)
```

## Common Tasks

### Task 1: Geocode Single Address
```python
from config import Config
from geocoder import CensusGeocoder

config = Config()
geocoder = CensusGeocoder(config.get_census_url())
county = geocoder.geocode_address("123 Main St", "Atlanta", "GA", "30301")
print(f"County: {county}")
```

### Task 2: Process CSV File
```python
from config import Config
from geocoder import CensusGeocoder
from data_processor import CountyDataProcessor

config = Config()
geocoder = CensusGeocoder(config.get_census_url())
processor = CountyDataProcessor(geocoder)
processor.process_csv_file("input.csv", "output.csv")
```

### Task 3: Analyze Results
```python
from utils import DataAnalyzer

# Generate full report
DataAnalyzer.generate_report("output.csv")

# Get statistics dict
stats = DataAnalyzer.analyze_csv("output.csv")
print(stats['counties'])
```

### Task 4: Export by County
```python
from utils import DataAnalyzer

files = DataAnalyzer.export_by_county("output.csv", "Data/by_county")
print(f"Created {len(files)} files")
```

## Class Reference

### Config
- `get_census_url()` → str
- `get_api_delay()` → float

### CensusGeocoder
- `__init__(api_url, delay=0.5)`
- `geocode_address(street, city, state, zip)` → str | None
- `wait()` → None

### CountyDataProcessor
- `__init__(geocoder)`
- `load_csv(filepath)` → DataFrame
- `identify_missing_counties(df)` → DataFrame
- `process_row(idx, row, df, progress_num, total)` → bool
- `process_dataframe(df, callback=None)` → DataFrame
- `save_csv(df, filepath)` → None
- `print_summary()` → None
- `process_csv_file(input_file, output_file)` → None

### DataAnalyzer
- `analyze_csv(filepath)` → Dict
- `compare_csvs(original, updated)` → Dict
- `export_by_county(input_file, output_dir)` → List[str]
- `generate_report(filepath, output_file=None)` → None

### DataCleaner
- `clean_phone_numbers(df)` → DataFrame
- `normalize_addresses(df)` → DataFrame
- `fill_missing_values(df, defaults)` → DataFrame

## Environment Variables

```env
# Required
CENSUS_URL="https://geocoding.geo.census.gov/geocoder/geographies/address"

# Optional
API_DELAY="0.5"
MONGO_URI="mongodb+srv://..."
DB_NAME="GA"
COLLECTION_NAME="properties"
```

## Error Handling

### Handle Missing Config
```python
try:
    config = Config()
except ValueError as e:
    print(f"Configuration error: {e}")
```

### Handle Geocoding Failures
```python
county = geocoder.geocode_address(...)
if county:
    print(f"Found: {county}")
else:
    print("Geocoding failed")
```

### Handle CSV Errors
```python
try:
    df = processor.load_csv("file.csv")
except FileNotFoundError:
    print("File not found")
```

## Extension Patterns

### Custom Geocoder
```python
class MyGeocoder(CensusGeocoder):
    def geocode_address(self, *args):
        # Custom logic
        return super().geocode_address(*args)
```

### Custom Processor
```python
class MyProcessor(CountyDataProcessor):
    def process_row(self, idx, row, df, progress_num, total):
        # Custom logic
        return super().process_row(idx, row, df, progress_num, total)
```

### Custom Analyzer
```python
class MyAnalyzer(DataAnalyzer):
    @staticmethod
    def my_custom_analysis(filepath):
        # Custom analysis
        pass
```

## Tips & Best Practices

1. **Always use Config class** for settings
2. **Handle None returns** from geocoder
3. **Use progress callbacks** for long operations
4. **Cache results** when processing same addresses
5. **Validate data** before processing
6. **Check CSV structure** matches expected format
7. **Monitor API rate limits** (default 0.5s delay)
8. **Review failed geocoding** results manually

## Troubleshooting

### Issue: "CENSUS_URL not found"
**Solution:** Check `.env` file format, ensure no spaces around `=`

### Issue: "Geocoding always returns None"
**Solution:** Check internet connection, verify Census API is accessible

### Issue: "KeyError: 'CountyName'"
**Solution:** Verify CSV has 'CountyName' column

### Issue: "Out of memory"
**Solution:** Process CSV in chunks for large files

## Performance Tips

1. Increase `API_DELAY` if getting rate limited
2. Use caching for repeated addresses
3. Process in parallel for multiple files
4. Consider async processing for large datasets
5. Use progress callbacks to monitor long operations
