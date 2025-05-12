import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))


import pandas
from flask import Flask, request, jsonify
import requests
from datetime import datetime
from utils import *

app = Flask(__name__)
path = "interest_rates.csv"
rate_dict = load_interest_rate(path)
compound_interest = calculate_compound_interest(rate_dict)


@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok"}), 200

@app.route("/refund", methods=["POST"])
def refund():
    request_data = request.get_json()
    pin = request_data["pin"].strip()

    endpoint = f"http://34.28.139.127:8082/comp?pin={pin}"
    response = requests.get(endpoint)
    if response.status_code != 200:
        return jsonify({"error": f"Failed to fetch comparables data. {response.text}"}), response.status_code
    
    try:
        # Get the retrieved data
        data = response.json()
        if not data:
            return jsonify({"error": f"No comparables returned for PIN '{pin}'"}), 404
        
        # Compute assessed values and compare them
        pins = list(data.keys())
        property_data = data[pins[0]]
        property_assessed_value = float(property_data["assessed value"])
        avg_assessed_values = calculate_avg_assessed_values(pin, pins, data)
        if property_assessed_value <= avg_assessed_values:
            return invalid_refunds(pin)

        # Determine full-year occupancy
        sale_year = datetime.strptime(property_data["sale date"], "%m/%d/%Y").year
        current_year = datetime.now().year
        full_years = current_year - sale_year
        years_eligible = min(4, full_years)
        if years_eligible < 0:
            return invalid_refunds(pin)

        # Calculate total refund amount
        total_refund = 0
        refund = property_assessed_value - avg_assessed_values
        for i in range(years_eligible):
            year = current_year - i - 1
            total_refund += refund * compound_interest[year]
        
        # Return JSON output
        return jsonify({
            "pin": pin,
            "yearsEligible": years_eligible,
            "totalRefund": round(total_refund, 2)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route("/market-change", methods=["GET"])
def market_value_change():
    pin = request.args.get("pin", "").strip()
    if not pin:
        return jsonify({"error": "PIN is required"}), 400


    try:
        url = f"https://www.cookcountyassessor.com/pin/{pin}"
        response = requests.get(url, timeout=10)
        print(response.status_code)
        if response.status_code != 200:
            if response.status_code == 500:
                return jsonify({"error": "Invalid PIN or property not found."}), response.status_code
            return jsonify({"error": f"Failed to fetch data. {response.text}"}), response.status_code
        
        result = get_market_value(pin, response)
        if not result:
            return jsonify({"error": "Total Estimated Market Value not found"}), 404

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5050)
