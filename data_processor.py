"""
Data processing module for handling CSV operations and county data extraction.
"""
import pandas as pd
from typing import Callable, Optional
from geocoder import CensusGeocoder


class CountyDataProcessor:
    """
    Processes property data and extracts county information using geocoding.
    """
    
    def __init__(self, geocoder: CensusGeocoder):
        """
        Initialize the data processor.
        
        Args:
            geocoder: An instance of CensusGeocoder
        """
        self.geocoder = geocoder
        self.stats = {
            'total': 0,
            'needs_geocoding': 0,
            'geocoded': 0,
            'failed': 0,
            'already_had_county': 0
        }
    
    def _needs_geocoding(self, county_value) -> bool:
        """
        Check if a county value needs geocoding.
        
        Args:
            county_value: The county field value
            
        Returns:
            True if geocoding is needed, False otherwise
        """
        if pd.isna(county_value):
            return True
        
        county_str = str(county_value).strip().upper()
        return county_str == '' or county_str == 'UNKNOWN'
    
    def load_csv(self, filepath: str) -> pd.DataFrame:
        """
        Load CSV file into a DataFrame.
        
        Args:
            filepath: Path to the CSV file
            
        Returns:
            Pandas DataFrame
        """
        print(f"Reading CSV file: {filepath}")
        df = pd.read_csv(filepath)
        self.stats['total'] = len(df)
        return df
    
    def identify_missing_counties(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Identify rows that need county geocoding.
        
        Args:
            df: DataFrame with property data
            
        Returns:
            DataFrame with only rows that need geocoding
        """
        # Check which rows need geocoding
        needs_geocoding = (
            df['CountyName'].isna() | 
            (df['CountyName'].astype(str).str.strip() == '') |
            (df['CountyName'].astype(str).str.upper() == 'UNKNOWN')
        )
        
        self.stats['needs_geocoding'] = needs_geocoding.sum()
        self.stats['already_had_county'] = len(df) - needs_geocoding.sum()
        
        print(f"Found {self.stats['needs_geocoding']} properties with missing or unknown county information")
        
        return df[needs_geocoding]
    
    def process_row(
        self,
        idx: int,
        row: pd.Series,
        df: pd.DataFrame,
        progress_num: int,
        total_to_process: int
    ) -> bool:
        """
        Process a single row to extract county information.
        
        Args:
            idx: DataFrame index of the row
            row: The row data
            df: The full DataFrame (to update)
            progress_num: Current progress number
            total_to_process: Total number of rows to process
            
        Returns:
            True if successfully geocoded, False otherwise
        """
        street_address = row['StreetAddress']
        city = row['City']
        state = row['State']
        zipcode = row['Zipcode']
        
        print(f"Geocoding {progress_num}/{total_to_process}: {street_address}, {city}, {state} {zipcode}")
        
        # Call the Census API
        county = self.geocoder.geocode_address(street_address, city, state, zipcode)
        
        if county:
            df.at[idx, 'CountyName'] = county
            self.stats['geocoded'] += 1
            print(f"  ✓ Found: {county}")
            return True
        else:
            self.stats['failed'] += 1
            print(f"  ✗ County not found")
            return False
    
    def process_dataframe(
        self,
        df: pd.DataFrame,
        progress_callback: Optional[Callable[[int, int], None]] = None
    ) -> pd.DataFrame:
        """
        Process the entire DataFrame to fill in missing county information.
        
        Args:
            df: DataFrame with property data
            progress_callback: Optional callback function for progress updates
            
        Returns:
            Updated DataFrame with county information
        """
        # Identify rows that need geocoding
        missing_df = self.identify_missing_counties(df)
        total_to_process = len(missing_df)
        
        # Process each row
        for progress_num, (idx, row) in enumerate(missing_df.iterrows(), 1):
            self.process_row(idx, row, df, progress_num, total_to_process)
            
            # Add delay to be respectful to the API
            self.geocoder.wait()
            
            # Call progress callback if provided
            if progress_callback:
                progress_callback(progress_num, total_to_process)
        
        return df
    
    def save_csv(self, df: pd.DataFrame, filepath: str):
        """
        Save DataFrame to CSV file.
        
        Args:
            df: DataFrame to save
            filepath: Output file path
        """
        print(f"\nSaving updated CSV to: {filepath}")
        df.to_csv(filepath, index=False)
    
    def print_summary(self):
        """Print processing summary statistics."""
        print(f"\nSummary:")
        print(f"  Total properties: {self.stats['total']}")
        print(f"  Successfully geocoded: {self.stats['geocoded']}")
        print(f"  Failed to geocode: {self.stats['failed']}")
        print(f"  Already had county: {self.stats['already_had_county']}")
    
    def process_csv_file(self, input_file: str, output_file: str):
        """
        Complete processing pipeline: load, process, and save CSV.
        
        Args:
            input_file: Path to input CSV file
            output_file: Path to output CSV file
        """
        # Load CSV
        df = self.load_csv(input_file)
        
        # Process DataFrame
        df = self.process_dataframe(df)
        
        # Save results
        self.save_csv(df, output_file)
        
        # Print summary
        self.print_summary()
