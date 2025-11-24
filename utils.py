"""
Utility functions and helper scripts for county data extraction.
"""
import pandas as pd
from typing import Dict, List
import json


class DataAnalyzer:
    """Analyze property data and generate reports."""
    
    @staticmethod
    def analyze_csv(filepath: str) -> Dict:
        """
        Analyze a CSV file and return statistics.
        
        Args:
            filepath: Path to CSV file
            
        Returns:
            Dictionary with analysis results
        """
        df = pd.read_csv(filepath)
        
        analysis = {
            'total_properties': len(df),
            'counties': {},
            'cities': {},
            'zipcodes': {},
            'property_types': {},
            'missing_county': 0,
            'price_stats': {}
        }
        
        # County analysis
        county_counts = df['CountyName'].value_counts()
        analysis['counties'] = county_counts.to_dict()
        analysis['missing_county'] = df['CountyName'].isna().sum()
        
        # City analysis
        city_counts = df['City'].value_counts()
        analysis['cities'] = city_counts.head(10).to_dict()
        
        # Zipcode analysis
        zipcode_counts = df['Zipcode'].value_counts()
        analysis['zipcodes'] = zipcode_counts.head(10).to_dict()
        
        # Property type analysis
        if 'HomeType' in df.columns:
            type_counts = df['HomeType'].value_counts()
            analysis['property_types'] = type_counts.to_dict()
        
        # Price statistics
        if 'Price' in df.columns:
            analysis['price_stats'] = {
                'mean': float(df['Price'].mean()),
                'median': float(df['Price'].median()),
                'min': float(df['Price'].min()),
                'max': float(df['Price'].max())
            }
        
        return analysis
    
    @staticmethod
    def compare_csvs(original_file: str, updated_file: str) -> Dict:
        """
        Compare original and updated CSV files.
        
        Args:
            original_file: Path to original CSV
            updated_file: Path to updated CSV
            
        Returns:
            Dictionary with comparison results
        """
        df_original = pd.read_csv(original_file)
        df_updated = pd.read_csv(updated_file)
        
        original_missing = df_original['CountyName'].isna().sum()
        updated_missing = df_updated['CountyName'].isna().sum()
        
        comparison = {
            'original_missing': int(original_missing),
            'updated_missing': int(updated_missing),
            'records_updated': int(original_missing - updated_missing),
            'success_rate': f"{((original_missing - updated_missing) / original_missing * 100):.1f}%"
        }
        
        return comparison
    
    @staticmethod
    def export_by_county(input_file: str, output_dir: str = "Data/by_county"):
        """
        Split CSV file into separate files by county.
        
        Args:
            input_file: Path to input CSV
            output_dir: Directory to save county-specific files
        """
        import os
        
        df = pd.read_csv(input_file)
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Group by county
        grouped = df.groupby('CountyName')
        
        files_created = []
        for county_name, group_df in grouped:
            if pd.notna(county_name):
                filename = f"{output_dir}/{county_name.replace(' ', '_')}.csv"
                group_df.to_csv(filename, index=False)
                files_created.append(filename)
                print(f"Created: {filename} ({len(group_df)} properties)")
        
        return files_created
    
    @staticmethod
    def generate_report(filepath: str, output_file: str = None):
        """
        Generate a detailed report from CSV data.
        
        Args:
            filepath: Path to CSV file
            output_file: Optional path to save report (JSON format)
        """
        analysis = DataAnalyzer.analyze_csv(filepath)
        
        print("\n" + "=" * 60)
        print("PROPERTY DATA ANALYSIS REPORT")
        print("=" * 60)
        
        print(f"\nTotal Properties: {analysis['total_properties']}")
        print(f"Missing County Data: {analysis['missing_county']}")
        
        print("\nTop Counties:")
        for county, count in list(analysis['counties'].items())[:5]:
            print(f"  {county}: {count}")
        
        print("\nTop Cities:")
        for city, count in list(analysis['cities'].items())[:5]:
            print(f"  {city}: {count}")
        
        print("\nTop Zip Codes:")
        for zipcode, count in list(analysis['zipcodes'].items())[:5]:
            print(f"  {zipcode}: {count}")
        
        if analysis['property_types']:
            print("\nProperty Types:")
            for ptype, count in analysis['property_types'].items():
                print(f"  {ptype}: {count}")
        
        if analysis['price_stats']:
            print("\nPrice Statistics:")
            print(f"  Mean: ${analysis['price_stats']['mean']:,.2f}")
            print(f"  Median: ${analysis['price_stats']['median']:,.2f}")
            print(f"  Min: ${analysis['price_stats']['min']:,.2f}")
            print(f"  Max: ${analysis['price_stats']['max']:,.2f}")
        
        print("=" * 60)
        
        # Save to file if requested
        if output_file:
            with open(output_file, 'w') as f:
                json.dump(analysis, f, indent=2)
            print(f"\nReport saved to: {output_file}")


class DataCleaner:
    """Clean and normalize property data."""
    
    @staticmethod
    def clean_phone_numbers(df: pd.DataFrame) -> pd.DataFrame:
        """Clean and format phone numbers."""
        if 'BrokerPhoneNumber' in df.columns:
            df['BrokerPhoneNumber'] = df['BrokerPhoneNumber'].astype(str).str.replace(r'\D', '', regex=True)
        return df
    
    @staticmethod
    def normalize_addresses(df: pd.DataFrame) -> pd.DataFrame:
        """Normalize street addresses."""
        if 'StreetAddress' in df.columns:
            df['StreetAddress'] = df['StreetAddress'].str.strip().str.title()
        return df
    
    @staticmethod
    def fill_missing_values(df: pd.DataFrame, defaults: Dict = None) -> pd.DataFrame:
        """Fill missing values with defaults."""
        if defaults:
            for column, default_value in defaults.items():
                if column in df.columns:
                    df[column].fillna(default_value, inplace=True)
        return df


def cli_analyze():
    """CLI command to analyze a CSV file."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python utils.py <csv_file>")
        return
    
    filepath = sys.argv[1]
    DataAnalyzer.generate_report(filepath)


def cli_compare():
    """CLI command to compare two CSV files."""
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python utils.py compare <original_file> <updated_file>")
        return
    
    original = sys.argv[2]
    updated = sys.argv[3]
    
    comparison = DataAnalyzer.compare_csvs(original, updated)
    
    print("\n" + "=" * 60)
    print("CSV COMPARISON REPORT")
    print("=" * 60)
    print(f"Original missing: {comparison['original_missing']}")
    print(f"Updated missing: {comparison['updated_missing']}")
    print(f"Records updated: {comparison['records_updated']}")
    print(f"Success rate: {comparison['success_rate']}")
    print("=" * 60)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "compare":
            cli_compare()
        else:
            cli_analyze()
    else:
        print("County Data Extraction Utilities")
        print("=" * 60)
        print("Available commands:")
        print("  python utils.py <csv_file>                    - Analyze CSV")
        print("  python utils.py compare <original> <updated>  - Compare CSVs")
