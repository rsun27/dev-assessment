import pandas as pd
import requests

def fetch_refund(pin):
    try:
        r = requests.post("http://127.0.0.1:5050/refund", json={"pin": pin}, timeout=10)
        if r.status_code == 200:
            return r.json().get("yearsEligible"), r.json().get("totalRefund"), ""
        else:
            try:
                return None, None, r.json().get("error", "Refund error")
            except ValueError:
                return None, None, "Invalid response from refund service"
    except Exception as e:
        return None, None, str(e)

def fetch_market(pin):
    try:
        r = requests.get(f"http://127.0.0.1:5050/market-change?pin={pin}", timeout=10)
        if r.status_code == 200:
            data = r.json()
            return data["currentMarketValue"], data["previousMarketValue"], data["percentChange"], ""
        else:
            try:
                return None, None, None, r.json().get("error", "Market error")
            except ValueError:
                return None, None, None, "Invalid response from market service"
    except Exception as e:
        return None, None, None, str(e)


def process_pins(input_file, output_file):
    df = pd.read_csv(input_file, dtype={"PIN": str})
    pins = df["PIN"].to_list()
    results = []

    for pin in pins:
        refund_years, refund_amount, refund_error = fetch_refund(pin)
        current_mv, previous_mv, percent_change, market_error = fetch_market(pin)

        results.append({
            "pin": pin,
            "yearsEligible": refund_years,
            "totalRefund": refund_amount,
            "currentMarketValue": current_mv,
            "previousMarketValue": previous_mv,
            "percentChange": percent_change,
        })

    result_df = pd.DataFrame(results)
    result_df.to_csv(output_file, index=False)
    print(f"Saved results to {output_file}")

if __name__ == "__main__":
    process_pins("pins.csv", "results.csv")

