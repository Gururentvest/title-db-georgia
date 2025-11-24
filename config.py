"""
Configuration module for loading environment variables and settings.
"""
import os
from dotenv import load_dotenv


class Config:
    """Configuration class for managing application settings."""
    
    def __init__(self):
        """Load environment variables."""
        load_dotenv()
        
        # API Configuration
        self.census_url = os.getenv('CENSUS_URL')
        self.fulton_county_url = os.getenv('FULTON_COUNTY_URL')
        self.dekalb_county_url = os.getenv('DEALB_COUNTY_URL')
        
        # Database Configuration
        self.mongo_uri = os.getenv('MONGO_URI')
        self.db_name = os.getenv('DB_NAME')
        self.collection_name = os.getenv('COLLECTION_NAME')
        
        # API Rate Limiting
        self.api_delay = float(os.getenv('API_DELAY', '0.5'))
        
        # Validate required settings
        self._validate()
    
    def _validate(self):
        """Validate that required configuration is present."""
        if not self.census_url:
            raise ValueError("CENSUS_URL not found in .env file")
    
    def get_census_url(self) -> str:
        """Get the Census API URL."""
        return self.census_url
    
    def get_api_delay(self) -> float:
        """Get the API delay setting."""
        return self.api_delay
