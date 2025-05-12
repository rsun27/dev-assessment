# Property Tax Refund API

This is a containerized Flask-based API service that calculates property tax refunds using comparables data and historical interest rates. It provides a RESTful `/refund` endpoint and includes automated tests and CSV batch processing support.

---

## 📁 Project Structure

```
dev-assessment/
│
├── app/
│   └── main.py              # Flask application with /refund and /market-change endpoints
│
├── test/
│   └── test.py              # Unit tests for refund logic
│
├── test_cases.py            # Mock responses and test payloads
├── utils.py                 # Utility functions for parsing rates, values, etc.
├── process_pins.py          # Batch processor for multiple PINs using the API
├── interest_rates.csv       # Yearly interest rate table
├── requirements.txt         # Python dependencies
├── Dockerfile               # Docker build instructions
└── README.md                # Project instructions (this file)
```

---

## 🚀 Setup and Run (Docker)

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

## 🧪 API Usage

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

---

## 🧪 Running Tests

You can run the unit tests outside Docker from the root directory:

```bash
python3 test/test.py
```

Or using unittest discovery:

```bash
python3 -m unittest discover -s test -p "*.py"
```

---

## 📊 Batch Mode (Optional)

To compute refunds and market values for a list of PINs from a CSV:

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

## ⚙️ Environment Variables (Optional)

You can override API host settings:

| Variable       | Default               | Description                   |
|----------------|------------------------|-------------------------------|
| `PORT`         | `5000`                 | Port Flask runs on            |
| `API_BASE_URL` | `http://127.0.0.1:5000`| Used by `process_pins.py`     |

---

## 📝 Notes

- This service calls a live comparables endpoint at `http://34.28.139.127:8082/comp?pin=...`
- Only full calendar years (up to 4) are used for refund eligibility.
- Refunds are adjusted to present value using compound interest from `interest_rates.csv`.

---

## 📄 License

MIT License (or replace with your organization’s policy)