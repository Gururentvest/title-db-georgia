"""
Main entry point for the county data extraction application.
"""
from config import Config
from geocoder import CensusGeocoder
from data_processor import CountyDataProcessor


def main():
    """Main function to run the county data extraction."""
    # Define input and output file paths
    input_file = "Data/ForRentByOwner_Contact_2025-09-02_withID - Guru.csv"
    output_file = "Data/ForRentByOwner_Contact_2025-09-02_withID - Guru_with_counties.csv"
    
    try:
        # Load configuration
        config = Config()
        
        # Initialize geocoder with Census API
        geocoder = CensusGeocoder(
            api_url=config.get_census_url(),
            delay=config.get_api_delay()
        )
        
        # Initialize data processor
        processor = CountyDataProcessor(geocoder)
        
        # Process the CSV file
        processor.process_csv_file(input_file, output_file)
        
        print("\n✓ Processing complete!")
    except Exception as e:
        print(f"\n✗ Error: {e}")
        raise


if __name__ == "__main__":
    main()
