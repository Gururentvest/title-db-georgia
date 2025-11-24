# Modular Architecture Overview

## Project Structure

```
title-db-georgia/
├── main.py              # Main entry point - orchestrates the workflow
├── config.py            # Configuration management (env variables)
├── geocoder.py          # Census API geocoding logic
├── data_processor.py    # CSV processing and data extraction
├── utils.py             # Utility functions and data analysis
├── examples.py          # Usage examples and tutorials
├── .env                 # Environment variables
├── pyproject.toml       # Project dependencies
├── README.md            # Project documentation
└── Data/                # Data directory
```

## Core Modules

### 1. **config.py** - Configuration Management
**Purpose:** Centralized configuration and environment variable management

**Key Components:**
- `Config` class: Loads and validates environment variables
- Provides typed access to configuration values
- Validates required settings on initialization

**Usage:**
```python
from config import Config

config = Config()
census_url = config.get_census_url()
api_delay = config.get_api_delay()
```

---

### 2. **geocoder.py** - Geocoding Service
**Purpose:** Handles all interactions with the U.S. Census Geocoder API

**Key Components:**
- `CensusGeocoder` class: Wrapper for Census API
- Rate limiting with configurable delays
- Error handling and retry logic
- Extensible for custom geocoding implementations

**Usage:**
```python
from geocoder import CensusGeocoder

geocoder = CensusGeocoder(api_url="https://...", delay=0.5)
county = geocoder.geocode_address("123 Main St", "Atlanta", "GA", "30301")
```

**Features:**
- Automatic retry on network errors
- Configurable timeout and delay
- Clean error messages
- Returns `None` for failed geocoding (no exceptions thrown)

---

### 3. **data_processor.py** - Data Processing Pipeline
**Purpose:** Handles CSV operations and orchestrates the county extraction workflow

**Key Components:**
- `CountyDataProcessor` class: Main data processing engine
- CSV loading and saving
- Identifies rows needing geocoding
- Progress tracking and statistics
- Batch processing with callbacks

**Usage:**
```python
from data_processor import CountyDataProcessor

processor = CountyDataProcessor(geocoder)
processor.process_csv_file("input.csv", "output.csv")
```

**Features:**
- Automatic detection of missing county data
- Progress reporting
- Statistics collection
- Extensible for custom processing logic
- Support for progress callbacks

---

### 4. **utils.py** - Utility Functions
**Purpose:** Analysis, reporting, and data cleaning utilities

**Key Components:**
- `DataAnalyzer`: Statistical analysis and reporting
  - `analyze_csv()`: Generate detailed statistics
  - `compare_csvs()`: Compare before/after processing
  - `export_by_county()`: Split data by county
  - `generate_report()`: Create formatted reports

- `DataCleaner`: Data cleaning and normalization
  - `clean_phone_numbers()`: Format phone numbers
  - `normalize_addresses()`: Standardize addresses
  - `fill_missing_values()`: Fill defaults

**Usage:**
```python
from utils import DataAnalyzer

# Generate analysis report
DataAnalyzer.generate_report("data.csv")

# Compare files
comparison = DataAnalyzer.compare_csvs("original.csv", "updated.csv")
```

**CLI Commands:**
```bash
# Analyze a CSV file
uv run python utils.py "data.csv"

# Compare two CSV files
uv run python utils.py compare "original.csv" "updated.csv"
```

---

### 5. **main.py** - Application Entry Point
**Purpose:** Orchestrates the entire county extraction process

**Workflow:**
1. Load configuration from `.env`
2. Initialize geocoder with Census API
3. Create data processor
4. Process CSV file (load → geocode → save)
5. Display results and statistics

**Usage:**
```bash
uv run main.py
```

---

### 6. **examples.py** - Usage Examples
**Purpose:** Demonstrates various ways to use the modules

**Examples Included:**
1. Simple single address geocoding
2. Batch geocoding multiple addresses
3. Custom CSV processing with manual control
4. Using progress callbacks
5. Manual data manipulation
6. Creating custom geocoder classes with caching

**Usage:**
```bash
uv run python examples.py
```

---

## Benefits of Modular Design

### 1. **Separation of Concerns**
- Each module has a single, well-defined responsibility
- Easy to understand and maintain
- Changes in one module don't affect others

### 2. **Reusability**
- Use `geocoder.py` in other projects
- Reuse `data_processor.py` for different data sources
- Mix and match components as needed

### 3. **Testability**
- Each module can be tested independently
- Mock dependencies easily
- Write focused unit tests

### 4. **Extensibility**
- Extend `CensusGeocoder` for custom behavior
- Subclass `CountyDataProcessor` for custom logic
- Add new analyzers to `utils.py`

### 5. **Maintainability**
- Clear module boundaries
- Easy to locate and fix bugs
- Simple to add new features

---

## Extension Examples

### Custom Geocoder with Caching
```python
from geocoder import CensusGeocoder

class CachedGeocoder(CensusGeocoder):
    def __init__(self, api_url, delay=0.5):
        super().__init__(api_url, delay)
        self.cache = {}
    
    def geocode_address(self, street, city, state, zip):
        key = f"{street}|{city}|{state}|{zip}"
        if key not in self.cache:
            self.cache[key] = super().geocode_address(street, city, state, zip)
        return self.cache[key]
```

### Custom Data Processor
```python
from data_processor import CountyDataProcessor

class CustomProcessor(CountyDataProcessor):
    def process_row(self, idx, row, df, progress_num, total):
        # Custom preprocessing
        if row['City'] == 'Atlanta':
            # Custom logic for Atlanta
            pass
        return super().process_row(idx, row, df, progress_num, total)
```

### Custom Analysis
```python
from utils import DataAnalyzer

class CustomAnalyzer(DataAnalyzer):
    @staticmethod
    def analyze_price_by_county(filepath):
        df = pd.read_csv(filepath)
        return df.groupby('CountyName')['Price'].agg(['mean', 'median', 'count'])
```

---

## Configuration Options

### Environment Variables (.env)
```env
# Required
CENSUS_URL="https://geocoding.geo.census.gov/geocoder/geographies/address"

# Optional
API_DELAY="0.5"                    # Delay between API calls (seconds)
MONGO_URI="mongodb+srv://..."      # Database connection (if needed)
DB_NAME="GA"                       # Database name
COLLECTION_NAME="properties"       # Collection name
```

---

## Error Handling

### Geocoder Errors
- Network failures → Returns `None`, logs error
- Invalid addresses → Returns `None`, no error
- API timeouts → Returns `None` after 10 seconds

### Configuration Errors
- Missing required variables → Raises `ValueError` immediately
- Invalid values → Raises `ValueError` with description

### Data Processing Errors
- Invalid CSV → Raises `FileNotFoundError`
- Missing columns → Raises `KeyError` with column name
- Type errors → Raises `TypeError` with details

---

## Performance Considerations

1. **API Rate Limiting**: Default 0.5s delay between requests
2. **Batch Processing**: Processes all rows in one pass
3. **Memory Usage**: Loads entire CSV into memory (use chunking for large files)
4. **Caching**: Implement custom geocoder with cache for repeated addresses

---

## Future Enhancements

### Potential Additions:
1. **Database Integration**: Save results to MongoDB
2. **Async Processing**: Use `asyncio` for concurrent API calls
3. **Retry Logic**: Automatic retry for failed geocoding
4. **Progress Bar**: Visual progress indicator
5. **Logging**: Structured logging with levels
6. **Web Interface**: Flask/FastAPI web UI
7. **Batch Export**: Export to multiple formats (JSON, Excel)
8. **Data Validation**: Schema validation for input data

---

## Quick Start Guide

### Basic Usage
```bash
# 1. Install dependencies
uv sync

# 2. Configure .env file
# Edit .env with your settings

# 3. Run the main script
uv run main.py

# 4. View results
# Check Data/ folder for output file
```

### Advanced Usage
```python
# Import modules
from config import Config
from geocoder import CensusGeocoder
from data_processor import CountyDataProcessor

# Setup
config = Config()
geocoder = CensusGeocoder(config.get_census_url())
processor = CountyDataProcessor(geocoder)

# Process data
df = processor.load_csv("input.csv")
df = processor.process_dataframe(df)
processor.save_csv(df, "output.csv")
processor.print_summary()
```

---

## Testing

### Unit Tests (Example)
```python
# test_geocoder.py
from geocoder import CensusGeocoder

def test_valid_address():
    geocoder = CensusGeocoder("https://...", delay=0)
    county = geocoder.geocode_address("123 Main St", "Atlanta", "GA", "30301")
    assert county is not None

def test_invalid_address():
    geocoder = CensusGeocoder("https://...", delay=0)
    county = geocoder.geocode_address("Invalid", "Invalid", "XX", "00000")
    assert county is None
```

---

## Support

For issues or questions:
1. Check the documentation in each module
2. Review `examples.py` for usage patterns
3. Run `utils.py` for data analysis
4. Check error messages for specific issues

## License

See LICENSE file for details.
