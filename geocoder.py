"""
Geocoding module for US Census API integration.
"""
import requests
import time
from typing import Optional


class CensusGeocoder:
    """
    A geocoder class that uses the U.S. Census Geocoder API to retrieve
    county information for addresses.
    """
    
    def __init__(self, api_url: str, delay: float = 0.5):
        """
        Initialize the geocoder.
        
        Args:
            api_url: The U.S. Census Geocoder API endpoint URL
            delay: Delay in seconds between API calls (default: 0.5)
        """
        self.api_url = api_url
        self.delay = delay
    
    def geocode_address(
        self,
        street_address: str,
        city: str,
        state: str,
        zipcode: str
    ) -> Optional[str]:
        """
        Geocode an address using the U.S. Census Geocoder API.
        
        Args:
            street_address: Street address
            city: City name
            state: State abbreviation (e.g., 'GA')
            zipcode: ZIP code
            
        Returns:
            County name if found, otherwise None
        """
        try:
            # Construct the parameters for the API request
            params = {
                'street': street_address,
                'city': city,
                'state': state,
                'zip': zipcode,
                'benchmark': 'Public_AR_Current',
                'vintage': 'Current_Current',
                'format': 'json'
            }
            
            # Make the API request
            response = requests.get(self.api_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Extract county information from the response
            if 'result' in data and 'addressMatches' in data['result']:
                matches = data['result']['addressMatches']
                if matches and len(matches) > 0:
                    # Get the first match
                    match = matches[0]
                    if 'geographies' in match and 'Counties' in match['geographies']:
                        counties = match['geographies']['Counties']
                        if counties and len(counties) > 0:
                            county_name = counties[0].get('NAME', '')
                            return county_name
            
            return None
        
        except requests.exceptions.RequestException as e:
            print(f"Error geocoding {street_address}: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error for {street_address}: {e}")
            return None
    
    def wait(self):
        """Add a delay to be respectful to the API."""
        time.sleep(self.delay)
