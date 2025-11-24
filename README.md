# Title DB Georgia - County Data Extraction

A modular Python application for extracting county information from property addresses using the U.S. Census Geocoder API.

## Project Structure

```
title-db-georgia/
├── main.py              # Main entry point
├── config.py            # Configuration management
├── geocoder.py          # Census API geocoding logic
├── data_processor.py    # CSV processing and data extraction
├── .env                 # Environment variables
├── pyproject.toml       # Project dependencies
└── Data/               # Data directory
```

## Modules

### 1. `config.py` - Configuration Management
Handles loading and validation of environment variables from `.env` file.

**Key Features:**
- Loads Census API URL
- Validates required configuration
- Manages API rate limiting settings

**Usage:**
```python
from config import Config

config = Config()
census_url = config.get_census_url()
```

### 2. `geocoder.py` - Census Geocoding
Handles interaction with the U.S. Census Geocoder API.

**Key Features:**
- Geocodes addresses to county information
- Handles API errors gracefully
- Implements rate limiting

**Usage:**
```python
from geocoder import CensusGeocoder

geocoder = CensusGeocoder(api_url="https://...", delay=0.5)
county = geocoder.geocode_address("123 Main St", "Atlanta", "GA", "30301")
```

### 3. `data_processor.py` - Data Processing
Processes CSV files and manages the county extraction workflow.

**Key Features:**
- Loads and saves CSV files
- Identifies rows needing geocoding
- Processes data with progress tracking
- Generates statistics and summaries

**Usage:**
```python
from data_processor import CountyDataProcessor

processor = CountyDataProcessor(geocoder)
processor.process_csv_file("input.csv", "output.csv")
```

### 4. `main.py` - Application Entry Point
Orchestrates the entire county extraction process.

**Features:**
- Initializes all components
- Runs the complete processing pipeline
- Handles errors and provides user feedback

## Installation

1. Install dependencies:
```bash
uv sync
```

## Configuration

Edit the `.env` file to configure:

```env
# Census API URL
CENSUS_URL="https://geocoding.geo.census.gov/geocoder/geographies/address"

# API delay between requests (seconds)
API_DELAY="0.5"

# Database configuration (optional)
MONGO_URI="mongodb+srv://..."
DB_NAME="GA"
COLLECTION_NAME="properties"
```

## Usage

Run the main script:

```bash
uv run main.py
```

The script will:
1. Read the input CSV file
2. Identify properties with missing county information
3. Geocode addresses using the Census API
4. Fill in county names
5. Save the updated CSV file
6. Display processing statistics

## Output

- **Input:** `Data/ForRentByOwner_Contact_2025-09-02_withID - Guru.csv`
- **Output:** `Data/ForRentByOwner_Contact_2025-09-02_withID - Guru_with_counties.csv`

## Features

- ✅ Modular architecture for easy maintenance
- ✅ Configurable via environment variables
- ✅ Rate-limited API requests
- ✅ Comprehensive error handling
- ✅ Progress tracking and statistics
- ✅ Reusable components

## Example Output

```
Reading CSV file: Data/ForRentByOwner_Contact_2025-09-02_withID - Guru.csv
Found 127 properties with missing or unknown county information
Geocoding 1/127: 2651 Avon Cv, Atlanta, GA 30329
  ✓ Found: DeKalb County
...
Saving updated CSV to: Data/ForRentByOwner_Contact_2025-09-02_withID - Guru_with_counties.csv

Summary:
  Total properties: 127
  Successfully geocoded: 120
  Failed to geocode: 7
  Already had county: 0

✓ Processing complete!
```

## Extending the Application

### Adding New Data Sources

Create a new processor class in `data_processor.py`:

```python
class CustomDataProcessor(CountyDataProcessor):
    def process_custom_format(self, data):
        # Custom processing logic
        pass
```

### Using Different Geocoding Services

Create a new geocoder class in `geocoder.py`:

```python
class CustomGeocoder:
    def geocode_address(self, street, city, state, zip):
        # Custom geocoding logic
        pass
```

## License

See LICENSE file for details.
