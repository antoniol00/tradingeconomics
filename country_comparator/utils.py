# utils.py
import requests
import matplotlib.pyplot as plt
import os
from config import TRADING_ECONOMICS_API_KEY

REFERENCE_VALUES = {
    "GDP": 10000,  # Example: GDP in millions
    "Inflation Rate": 20,  # A high-end benchmark for inflation
    "Unemployment Rate": 25,  # A high-end benchmark for unemployment
    "Balance of Trade": 500000,  # Example: Trade balance in millions
    "Consumer Confidence": 150,  # Typical range for confidence index
    "Corruption Rank": 200,  # Most corrupt country rank (higher is worse)
    "GDP per Capita": 100000,  # Example: GDP per capita
    "GDP per Capita PPP": 100000,  # Example: GDP per capita PPP
    "Lending Rate": 30,  # A high-end benchmark for lending rates
    "Productivity": 500,  # Arbitrary benchmark
    "Sales Tax Rate": 30,  # A high-end sales tax
    "Terrorism Index": 10,  # Terrorism Index range
    "Average Hourly Wages": 50,  # Example: max expected hourly wages
    "Youth Unemployment Rate": 50  # A high-end benchmark for youth unemployment
}

def get_economic_indicators(country):
    """
    Fetch economic indicators for the given country.
    
    Returns a dictionary where each indicator contains:
       - "value": Latest numeric value (or None)
       - "unit": Unit of measurement
       - "percentage": The value normalized as a percentage of a reference value
    """
    url = f'https://api.tradingeconomics.com/country/{country}?c={TRADING_ECONOMICS_API_KEY}'
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()  # A list of dictionaries

        # Define desired indicators with expected title formats
        desired_indicators = [
            (f'{country} gdp', 'GDP'),
            (f'{country} inflation rate', 'Inflation Rate'),
            (f'{country} unemployment rate', 'Unemployment Rate'),
            (f'{country} balance of trade', 'Balance of Trade'),
            (f'{country} consumer confidence', 'Consumer Confidence'),
            (f'{country} corruption rank', 'Corruption Rank'),
            (f'{country} gdp per capita', 'GDP per Capita'),
            (f'{country} gdp per capita ppp', 'GDP per Capita PPP'),
            (f'{country} lending rate', 'Lending Rate'),
            (f'{country} productivity', 'Productivity'),
            (f'{country} sales tax rate', 'Sales Tax Rate'),
            (f'{country} terrorism index', 'Terrorism Index'),
            (f'{country} average hourly wages', 'Average Hourly Wages'),
            (f'{country} youth unemployment rate', 'Youth Unemployment Rate')
        ]

        results = {}

        # Process each indicator
        for search_kw, display_name in desired_indicators:
            for item in data:
                title = item.get('Title', '')

                if search_kw.lower() in title.lower():
                    try:
                        value = float(item.get('LatestValue'))
                    except (ValueError, TypeError):
                        value = None

                    unit = item.get('Unit', '')
                    if unit == 'percent':
                        unit = '%'

                    # Calculate percentage based on reference value
                    reference_value = REFERENCE_VALUES.get(display_name, 1)  # Default to 1 to avoid division errors
                    percentage = (value / reference_value) * 100 if value is not None else None

                    # Store results
                    results[display_name] = {
                        "value": value,
                        "unit": unit,
                        "percentage": percentage
                    }
                    break  # Stop searching once we find the first match

            # If no match was found, store None
            if display_name not in results:
                results[display_name] = {"value": None, "unit": "", "percentage": None}

        return results
    else:
        return {}
