# Module Dependency Diagram

## Visual Architecture

```
┌────────────────────────────────────────────────────────────────────┐
│                                                                    │
│                          main.py                                   │
│                    (Entry Point - 37 lines)                        │
│                                                                    │
│  ┌──────────────────────────────────────────────────────────┐    │
│  │  1. Load Config                                          │    │
│  │  2. Initialize Geocoder                                  │    │
│  │  3. Create Processor                                     │    │
│  │  4. Process CSV                                          │    │
│  │  5. Display Results                                      │    │
│  └──────────────────────────────────────────────────────────┘    │
│                                                                    │
└────────────────────────┬───────────────────────────────────────────┘
                         │
         ┌───────────────┼───────────────┬───────────────┐
         │               │               │               │
         ▼               ▼               ▼               ▼
    ┌─────────┐   ┌──────────┐   ┌────────────┐   ┌────────┐
    │ config  │   │ geocoder │   │    data    │   │ utils  │
    │  .py    │   │   .py    │   │ processor  │   │  .py   │
    └─────────┘   └──────────┘   │   .py      │   └────────┘
         │               │        └────────────┘        │
         │               │               │              │
         │               └───────────────┘              │
         │                       │                      │
         └───────────────────────┴──────────────────────┘
                                 │
                                 ▼
                          External APIs
                     ┌─────────────────────┐
                     │  U.S. Census API    │
                     │  (Geocoding)        │
                     └─────────────────────┘
```

## Module Relationships

### 1. config.py
```
┌─────────────────────────────────────┐
│          config.py                  │
├─────────────────────────────────────┤
│  Class: Config                      │
│                                     │
│  Dependencies:                      │
│  • os (standard)                    │
│  • dotenv (external)                │
│                                     │
│  Provides:                          │
│  • get_census_url()                 │
│  • get_api_delay()                  │
│  • Configuration validation         │
│                                     │
│  Used by:                           │
│  • main.py                          │
│  • examples.py                      │
└─────────────────────────────────────┘
```

### 2. geocoder.py
```
┌─────────────────────────────────────┐
│        geocoder.py                  │
├─────────────────────────────────────┤
│  Class: CensusGeocoder              │
│                                     │
│  Dependencies:                      │
│  • requests (external)              │
│  • time (standard)                  │
│                                     │
│  Provides:                          │
│  • geocode_address()                │
│  • wait()                           │
│  • API error handling               │
│                                     │
│  Used by:                           │
│  • data_processor.py                │
│  • main.py                          │
│  • examples.py                      │
└─────────────────────────────────────┘
```

### 3. data_processor.py
```
┌─────────────────────────────────────┐
│      data_processor.py              │
├─────────────────────────────────────┤
│  Class: CountyDataProcessor         │
│                                     │
│  Dependencies:                      │
│  • pandas (external)                │
│  • geocoder (internal)              │
│                                     │
│  Provides:                          │
│  • load_csv()                       │
│  • identify_missing_counties()      │
│  • process_row()                    │
│  • process_dataframe()              │
│  • save_csv()                       │
│  • print_summary()                  │
│  • process_csv_file()               │
│                                     │
│  Used by:                           │
│  • main.py                          │
│  • examples.py                      │
└─────────────────────────────────────┘
```

### 4. utils.py
```
┌─────────────────────────────────────┐
│           utils.py                  │
├─────────────────────────────────────┤
│  Classes:                           │
│  • DataAnalyzer                     │
│  • DataCleaner                      │
│                                     │
│  Dependencies:                      │
│  • pandas (external)                │
│  • json (standard)                  │
│                                     │
│  Provides:                          │
│  • analyze_csv()                    │
│  • compare_csvs()                   │
│  • export_by_county()               │
│  • generate_report()                │
│  • Data cleaning utilities          │
│                                     │
│  Used by:                           │
│  • CLI commands                     │
│  • examples.py                      │
│  • Custom scripts                   │
└─────────────────────────────────────┘
```

## Data Flow Diagram

```
┌────────────┐
│   Input    │
│   CSV      │
└─────┬──────┘
      │
      ▼
┌─────────────────────────────────────────┐
│  data_processor.py                      │
│  ┌───────────────────────────────────┐  │
│  │ 1. Load CSV                       │  │
│  │    • Read file                    │  │
│  │    • Parse columns                │  │
│  └───────────────┬───────────────────┘  │
│                  │                      │
│  ┌───────────────▼───────────────────┐  │
│  │ 2. Identify Missing Counties      │  │
│  │    • Check for NaN                │  │
│  │    • Check for empty strings      │  │
│  │    • Check for "UNKNOWN"          │  │
│  └───────────────┬───────────────────┘  │
│                  │                      │
│  ┌───────────────▼───────────────────┐  │
│  │ 3. For Each Missing County        │◄─┐│
│  │    • Extract address              │  ││
│  │    • Call geocoder                │  ││
│  │    • Update DataFrame             │  ││
│  └───────────────┬───────────────────┘  ││
│                  │                      ││
│                  └──────────────────────┘│
│                                          │
│  ┌───────────────────────────────────┐  │
│  │ 4. Save Updated CSV               │  │
│  │    • Write to file                │  │
│  │    • Preserve formatting          │  │
│  └───────────────┬───────────────────┘  │
│                  │                      │
└──────────────────┼──────────────────────┘
                   │
      ┌────────────┼────────────┐
      │            │            │
      ▼            ▼            ▼
┌──────────┐ ┌──────────┐ ┌──────────┐
│ Output   │ │  Stats   │ │  Report  │
│  CSV     │ │  Summary │ │  (utils) │
└──────────┘ └──────────┘ └──────────┘
```

## Geocoding Process Flow

```
┌──────────────────────────────────────────────┐
│         geocoder.py                          │
│                                              │
│  ┌────────────────────────────────────────┐ │
│  │ Input: Address Components              │ │
│  │  • Street Address                      │ │
│  │  • City                                │ │
│  │  • State                               │ │
│  │  • ZIP Code                            │ │
│  └────────────────┬───────────────────────┘ │
│                   │                         │
│  ┌────────────────▼───────────────────────┐ │
│  │ Build API Request                      │ │
│  │  • Format parameters                   │ │
│  │  • Set benchmark & vintage             │ │
│  │  • Add timeout settings                │ │
│  └────────────────┬───────────────────────┘ │
│                   │                         │
│                   ▼                         │
│         ┌─────────────────┐                │
│         │  Census API     │                │
│         │  HTTP Request   │                │
│         └────────┬────────┘                │
│                  │                         │
│         ┌────────▼────────┐                │
│         │   Success?      │                │
│         └────┬───────┬────┘                │
│              │       │                     │
│         Yes  │       │  No                 │
│              │       │                     │
│  ┌───────────▼──┐ ┌──▼──────────────────┐ │
│  │ Parse JSON   │ │ Error Handling      │ │
│  │ Response     │ │  • Log error        │ │
│  │              │ │  • Return None      │ │
│  └───────┬──────┘ └──┬──────────────────┘ │
│          │           │                     │
│  ┌───────▼───────┐   │                     │
│  │ Extract       │   │                     │
│  │ County Name   │   │                     │
│  └───────┬───────┘   │                     │
│          │           │                     │
│  ┌───────▼───────────▼──────────────────┐ │
│  │ Return Result                         │ │
│  │  • County name (success)              │ │
│  │  • None (failure)                     │ │
│  └───────────────────────────────────────┘ │
│                                              │
└──────────────────────────────────────────────┘
```

## Class Hierarchy

```
Config
├── No inheritance
└── Standalone configuration class

CensusGeocoder
├── No inheritance (base class)
└── Can be extended:
    ├── CachedGeocoder (example)
    ├── RetryGeocoder (example)
    └── CustomGeocoder (user-defined)

CountyDataProcessor
├── No inheritance (base class)
└── Can be extended:
    ├── CustomProcessor (example)
    ├── BatchProcessor (example)
    └── AsyncProcessor (future)

DataAnalyzer
├── No inheritance
└── Static methods only

DataCleaner
├── No inheritance
└── Static methods only
```

## Module Communication

```
     User Command
         │
         ▼
   ┌─────────┐
   │ main.py │
   └────┬────┘
        │
        ├──> config.py ──> Environment Variables
        │
        ├──> geocoder.py ──> Census API
        │         │
        │         └──> HTTP Response
        │
        ├──> data_processor.py ──> CSV Files
        │         │
        │         └──> Updated CSV
        │
        └──> utils.py ──> Analysis Reports
                │
                └──> Statistics & Summaries
```

## File Dependencies

```
main.py
├── config.py
│   └── python-dotenv
├── geocoder.py
│   └── requests
└── data_processor.py
    ├── pandas
    └── geocoder.py

examples.py
├── config.py
├── geocoder.py
├── data_processor.py
└── pandas

utils.py
├── pandas
└── json (standard library)
```

## External Dependencies

```
Python Standard Library
├── os
├── time
├── json
└── sys

External Packages (pip/uv)
├── pandas (2.2.0+)
├── requests (2.31.0+)
└── python-dotenv (1.0.0+)

External Services
└── U.S. Census Geocoder API
    └── https://geocoding.geo.census.gov/
```

## Execution Flow

```
1. User runs: uv run main.py
             │
             ▼
2. main.py imports modules
   ├── config.py (loads .env)
   ├── geocoder.py
   └── data_processor.py
             │
             ▼
3. Initialize components
   ├── Config() → validates settings
   ├── CensusGeocoder() → sets up API client
   └── CountyDataProcessor() → ready to process
             │
             ▼
4. Process CSV file
   ├── Load CSV → DataFrame
   ├── Identify missing → 127 rows
   ├── For each row:
   │   ├── Geocode address
   │   ├── Wait 0.5s
   │   └── Update DataFrame
   └── Save CSV → Updated file
             │
             ▼
5. Display results
   ├── Total: 127
   ├── Success: 120
   └── Failed: 7
```

## Testing Flow

```
Manual Testing
├── Run main.py ✓
├── Run utils.py ✓
├── Run examples.py ✓
└── Verify outputs ✓

Automated Testing (Future)
├── Unit tests
│   ├── test_config.py
│   ├── test_geocoder.py
│   ├── test_data_processor.py
│   └── test_utils.py
└── Integration tests
    └── test_full_pipeline.py
```

---

This diagram shows the complete architecture and relationships between all modules in the county data extraction system.
