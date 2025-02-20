# utils.py
import requests
import matplotlib.pyplot as plt
import os
from config import TRADING_ECONOMICS_API_KEY

REFERENCE_VALUES = {
    "GDP": 10000,
    "Inflation Rate": 20, 
    "Unemployment Rate": 25,  
    "Balance of Trade": 500000,  
    "Consumer Confidence": 150,  
    "Corruption Index": 200,  
    "GDP per Capita": 100000, 
    "GDP per Capita PPP": 100000,  
    "Lending Rate": 30, 
    "Productivity": 500, 
    "Sales Tax Rate": 30, 
    "Terrorism Index": 10, 
    "Average Hourly Wages": 50, 
    "Youth Unemployment Rate": 50  
}

def get_economic_indicators(country):
    if TRADING_ECONOMICS_API_KEY == '': 
        url = f'https://api.tradingeconomics.com/country/{country}'
    else:
        url = f'https://api.tradingeconomics.com/country/{country}?c={TRADING_ECONOMICS_API_KEY}'
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()  # A list of dictionaries

        # Define desired indicators with expected title formats
        # Categorized economic indicators
        desired_indicators = [
            # Macro-Economic Indicators
            (f'{country} gdp', 'GDP'),
            (f'{country} gdp per capita', 'GDP per Capita'),
            (f'{country} gdp per capita ppp', 'GDP per Capita PPP'),
            
            # Inflation and Interest Rates
            (f'{country} inflation rate', 'Inflation Rate'),
            (f'{country} lending rate', 'Lending Rate'),
            
            # Labor Market
            (f'{country} unemployment rate', 'Unemployment Rate'),
            (f'{country} youth unemployment rate', 'Youth Unemployment Rate'),
            (f'{country} average hourly wages', 'Average Hourly Wages'),
            
            # Trade and Productivity
            (f'{country} balance of trade', 'Balance of Trade'),
            (f'{country} productivity', 'Productivity'),
            
            # Social and Confidence Metrics
            (f'{country} consumer confidence', 'Consumer Confidence'),
            (f'{country} corruption index', 'Corruption Index'),
            (f'{country} sales tax rate', 'Sales Tax Rate'),
            (f'{country} terrorism index', 'Terrorism Index')
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
    
# utils.py (modified sections at bottom)

HISTORICAL_MAPPING = {
    "GDP": "gdp",
    "Inflation Rate": "Core%20Inflation%20Rate",
    "Unemployment Rate": "Unemployment%20Rate",
    "Balance of Trade": "Balance%20of%20Trade",
    "Consumer Confidence": "Consumer%20Confidence",
    "Corruption Index": "Corruption%20Index",
    "GDP per Capita": "GDP%20per%20Capita",
    "GDP per Capita PPP": "GDP%20per%20Capita%20PPP",
    "Lending Rate": "Lending%20Rate",
    "Productivity": "Productivity",
    "Sales Tax Rate": "Sales%20Tax%20Rate",
    "Terrorism Index": "Terrorism%20Index",
    "Average Hourly Wages": "Wages",
    "Youth Unemployment Rate": "Youth%20Unemployment%20Rate"
}

def get_historical_indicator(country, display_indicator):
    slug = HISTORICAL_MAPPING.get(display_indicator)
    if not slug:
        return []
    if TRADING_ECONOMICS_API_KEY == '': 
        url = f'https://api.tradingeconomics.com/historical/country/{country}/indicator/{slug}'
    else:
        url = f'https://api.tradingeconomics.com/historical/country/{country}/indicator/{slug}?c={TRADING_ECONOMICS_API_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        # Expecting a list of dicts, each containing date and value.
        return response.json()
    else:
        return []
    



