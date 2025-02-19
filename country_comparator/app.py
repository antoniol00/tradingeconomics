# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
import requests
from config import TRADING_ECONOMICS_API_KEY, COUNTRY_INFO
from utils import get_economic_indicators
import os

app = Flask(__name__)
app.config.from_object('config')

# Available countries (fixed)
AVAILABLE_COUNTRIES = ["Sweden", "Mexico", "New Zealand", "Thailand"]

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

if __name__ == '__main__':
    app.run(debug=True)
