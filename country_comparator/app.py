# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
import requests
from config import TRADING_ECONOMICS_API_KEY, COUNTRY_INFO
from utils import get_economic_indicators, get_historical_indicator
import os

app = Flask(__name__)
app.config.from_object('config')

# Available countries (fixed)
AVAILABLE_COUNTRIES = [
    {"name": "Sweden", "flag": "https://flagcdn.com/se.svg"},
    {"name": "Mexico", "flag": "https://flagcdn.com/mx.svg"},
    {"name": "New Zealand", "flag": "https://flagcdn.com/nz.svg"},
    {"name": "Thailand", "flag": "https://flagcdn.com/th.svg"}
]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        country1 = request.form.get('country1')
        country2 = request.form.get('country2')
        if country1 == country2:
            flash("You cannot compare the same country. Please select two different countries.", "danger")
            return redirect(url_for('index'))
        return redirect(url_for('compare', country1=country1, country2=country2))
    return render_template('index.html', countries=AVAILABLE_COUNTRIES)

@app.route('/compare')
def compare():
    country1 = request.args.get('country1')
    country2 = request.args.get('country2')

    indicators1 = get_economic_indicators(country1)
    indicators2 = get_economic_indicators(country2)

    # Get country info (flag and location)
    country1_info = COUNTRY_INFO.get(country1, {})
    country2_info = COUNTRY_INFO.get(country2, {})

    return render_template('compare.html',
                           country1=country1, indicators1=indicators1,
                           country2=country2, indicators2=indicators2,
                           country1_info=country1_info,
                           country2_info=country2_info)

@app.route('/historical_data')
def historical_data():
    indicator = request.args.get('indicator')
    country1 = request.args.get('country1')
    country2 = request.args.get('country2')
    
    def simplify_series(series):
        simplified = []
        for item in series:
            try:
                value = float(item.get("Value", 0))
            except (ValueError, TypeError):
                value = 0
            simplified.append({
                "date": item.get("DateTime", "")[:10],
                "value": value
            })
        # Optionally sort by date if needed:
        simplified.sort(key=lambda x: x["date"])
        return simplified
    
    hist1_raw = get_historical_indicator(country1, indicator)
    hist2_raw = get_historical_indicator(country2, indicator)
    hist1 = simplify_series(hist1_raw)
    hist2 = simplify_series(hist2_raw)
    
    # remove last row in hist1 and hist2
    hist1 = hist1[:-1]
    hist2 = hist2[:-1]
    
    return {
        "data1": hist1,
        "data2": hist2
    }


if __name__ == '__main__':
    app.run(debug=True)
