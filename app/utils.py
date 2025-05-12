import pandas as pd
import numpy as np
from flask import jsonify
import requests
from bs4 import BeautifulSoup

def load_interest_rate(path):
    df = pd.read_csv(path)
    df = df.dropna(subset=['Year', 'Rate']) 
    df['Year'] = df['Year'].astype(int)
    rate_dict = dict(zip(df['Year'], df['Rate']))
    return rate_dict

def calculate_compound_interest(rate_dict):
    compound_interest = {}
    rate = 1
    for key, value in rate_dict.items():
        rate *= (1 + value)
        compound_interest[key] = rate
    return compound_interest


def is_valid_assessed_value(value):
        return not np.isnan(value) and value > 0


def calculate_avg_assessed_values(pin, pins, data):
    comparables_assessed_values = [float(data[p]["assessed value"]) for p in pins[1:] if is_valid_assessed_value(float(data[p]["assessed value"]))]
    if not comparables_assessed_values:
        return invalid_refunds(pin)
    
    avg_assessed_values = sum(comparables_assessed_values)/len(comparables_assessed_values)
    return avg_assessed_values


def invalid_refunds(pin):
    return jsonify({
        "pin": pin,
        "yearsEligible": 0,
        "totalRefund": 0.00
    })


def get_market_value(pin, response):
    try:
        soup = BeautifulSoup(response.text, "html.parser")
        rows = soup.find_all("div", class_="row pt-body equal-height")

        for row in rows:
            header = row.find("div", class_="col-xs-3 pt-header")
            if header and "Total Estimated Market Value" in header.text:
                values = row.find_all("div")[1:]
                current = float(values[0].text.strip().replace("$", "").replace(",", ""))
                previous = float(values[1].text.strip().replace("$", "").replace(",", ""))
                change = round((current - previous) / previous * 100, 2)
                
                return {
                    "pin": pin,
                    "currentMarketValue": current,
                    "previousMarketValue": previous,
                    "percentChange": f"{change}%"
                }
        return None 
    except Exception as e:
        raise RuntimeError(f"HTML parsing failed: {str(e)}")

