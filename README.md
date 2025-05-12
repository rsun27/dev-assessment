# Property Tax Refund API

This is a containerized Flask-based API service that calculates property tax refunds using comparables data and historical interest rates. It provides a RESTful `/refund` endpoint and includes automated tests and CSV batch processing support.

---

## Setup and Run (Docker)

### 1. Build the Docker image

```bash
docker build -t refund-service .
```

### 2. Run the container

```bash
docker run -p 5000:5000 refund-service
```

> This runs the Flask server and exposes the API on `http://localhost:5000`

---

## API Usage

### Refund Calculation Endpoint

**POST** `/refund`

```bash
curl -X POST http://localhost:5000/refund \
  -H "Content-Type: application/json" \
  -d '{"pin": "26062070090000"}'
```

**Response format**:
```json
{
  "pin": "26062070090000",
  "yearsEligible": 4,
  "totalRefund": 7043.40
}
```

### Market Value Change Endpoint

**GET** `/market-change?pin=<PIN>`

Example:

```bash
curl "http://localhost:5000/market-change?pin=26062070090000"

**Response format**:
```json
{ "pin": "26062070090000",
  "currentMarketValue": 293000.0,
  "previousMarketValue": 180000.0,
  "percentChange": "62.78%"
}
```

---

## Running Tests

You can run the unit tests outside Docker from the root directory:

```bash
python3 test/test.py
```
---

## Compute refunds and market values

1. Prepare a file called `pins.csv`:
```csv
PIN
26062070090000
1234567890
```

2. Run:

```bash
python3 process_pins.py
```

3. Results will be saved in `results.csv`.

---
