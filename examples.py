"""
Example scripts demonstrating how to use the modularized components.
"""
from config import Config
from geocoder import CensusGeocoder
from data_processor import CountyDataProcessor
import pandas as pd


def example_1_simple_geocoding():
    """Example 1: Simple geocoding of a single address."""
    print("=" * 60)
    print("Example 1: Simple Geocoding")
    print("=" * 60)
    
    # Load configuration
    config = Config()
    
    # Create geocoder
    geocoder = CensusGeocoder(
        api_url=config.get_census_url(),
        delay=0.5
    )
    
    # Geocode a single address
    county = geocoder.geocode_address(
        street_address="1600 Pennsylvania Avenue NW",
        city="Washington",
        state="DC",
        zipcode="20500"
    )
    
    print(f"County for White House: {county}")
    print()


def example_2_batch_geocoding():
    """Example 2: Batch geocoding of multiple addresses."""
    print("=" * 60)
    print("Example 2: Batch Geocoding")
    print("=" * 60)
    
    # Sample addresses
    addresses = [
        {"street": "1600 Pennsylvania Avenue NW", "city": "Washington", "state": "DC", "zip": "20500"},
        {"street": "350 Fifth Avenue", "city": "New York", "state": "NY", "zip": "10118"},
        {"street": "1 Infinite Loop", "city": "Cupertino", "state": "CA", "zip": "95014"},
    ]
    
    # Load configuration and create geocoder
    config = Config()
    geocoder = CensusGeocoder(config.get_census_url(), delay=0.5)
    
    # Geocode each address
    for addr in addresses:
        county = geocoder.geocode_address(
            street_address=addr["street"],
            city=addr["city"],
            state=addr["state"],
            zipcode=addr["zip"]
        )
        print(f"{addr['street']}, {addr['city']}: {county or 'Not found'}")
        geocoder.wait()
    
    print()


def example_3_custom_csv_processing():
    """Example 3: Custom CSV processing with custom logic."""
    print("=" * 60)
    print("Example 3: Custom CSV Processing")
    print("=" * 60)
    
    # Load configuration
    config = Config()
    geocoder = CensusGeocoder(config.get_census_url(), delay=0.5)
    
    # Create processor
    processor = CountyDataProcessor(geocoder)
    
    # Load CSV
    df = processor.load_csv("Data/ForRentByOwner_Contact_2025-09-02_withID - Guru.csv")
    
    # Get statistics
    missing_df = processor.identify_missing_counties(df)
    
    print(f"Total properties: {len(df)}")
    print(f"Properties needing geocoding: {len(missing_df)}")
    print(f"Properties with county data: {len(df) - len(missing_df)}")
    
    # You can now process the data manually or use the processor
    print()


def example_4_progress_callback():
    """Example 4: Using a progress callback."""
    print("=" * 60)
    print("Example 4: Progress Callback")
    print("=" * 60)
    
    def my_progress_callback(current, total):
        """Custom progress callback function."""
        percentage = (current / total) * 100
        print(f"Progress: {current}/{total} ({percentage:.1f}%)")
    
    # Load configuration
    config = Config()
    geocoder = CensusGeocoder(config.get_census_url(), delay=0.5)
    
    # Create processor
    processor = CountyDataProcessor(geocoder)
    
    # Load CSV
    df = processor.load_csv("Data/ForRentByOwner_Contact_2025-09-02_withID - Guru.csv")
    
    # Process with callback (limit to first 5 for demo)
    print("Processing first 5 properties with progress callback...")
    # Note: This is just a demonstration. In real use, you'd process the full dataset.
    print()


def example_5_manual_data_manipulation():
    """Example 5: Manual data manipulation using the modules."""
    print("=" * 60)
    print("Example 5: Manual Data Manipulation")
    print("=" * 60)
    
    # Load configuration
    config = Config()
    geocoder = CensusGeocoder(config.get_census_url(), delay=0.5)
    
    # Read CSV manually
    df = pd.read_csv("Data/ForRentByOwner_Contact_2025-09-02_withID - Guru.csv")
    
    # Filter for specific zip codes
    target_zipcodes = ['30329', '30309']
    filtered_df = df[df['Zipcode'].isin(target_zipcodes)]
    
    print(f"Properties in zip codes {target_zipcodes}: {len(filtered_df)}")
    
    # Count by zip code
    print("\nCounts by zip code:")
    print(filtered_df['Zipcode'].value_counts())
    print()


def example_6_custom_geocoder():
    """Example 6: Creating a custom geocoder wrapper."""
    print("=" * 60)
    print("Example 6: Custom Geocoder Wrapper")
    print("=" * 60)
    
    class CustomGeocoder(CensusGeocoder):
        """Extended geocoder with caching."""
        
        def __init__(self, api_url, delay=0.5):
            super().__init__(api_url, delay)
            self.cache = {}
        
        def geocode_address(self, street_address, city, state, zipcode):
            """Geocode with caching."""
            cache_key = f"{street_address}|{city}|{state}|{zipcode}"
            
            if cache_key in self.cache:
                print(f"  [CACHE HIT] {street_address}")
                return self.cache[cache_key]
            
            result = super().geocode_address(street_address, city, state, zipcode)
            self.cache[cache_key] = result
            return result
    
    # Use the custom geocoder
    config = Config()
    custom_geocoder = CustomGeocoder(config.get_census_url(), delay=0.5)
    
    # Test with same address twice
    address = "1600 Pennsylvania Avenue NW"
    
    county1 = custom_geocoder.geocode_address(address, "Washington", "DC", "20500")
    print(f"First call: {county1}")
    
    county2 = custom_geocoder.geocode_address(address, "Washington", "DC", "20500")
    print(f"Second call (cached): {county2}")
    print()


def main():
    """Run all examples."""
    print("\n")
    print("=" * 60)
    print("COUNTY DATA EXTRACTION - USAGE EXAMPLES")
    print("=" * 60)
    print()
    
    # Run examples
    try:
        example_1_simple_geocoding()
        example_2_batch_geocoding()
        example_3_custom_csv_processing()
        example_4_progress_callback()
        example_5_manual_data_manipulation()
        example_6_custom_geocoder()
        
        print("=" * 60)
        print("All examples completed!")
        print("=" * 60)
    except Exception as e:
        print(f"Error running examples: {e}")


if __name__ == "__main__":
    main()
