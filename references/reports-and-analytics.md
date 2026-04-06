# Sales & Finance Reports

Download sales, subscription, and financial reports as gzip-compressed TSV files.

## Sales Reports

```python
import gzip  # Additional imports required for report decompression
from io import BytesIO

response = requests.get(
    "https://api.appstoreconnect.apple.com/v1/salesReports",
    headers=headers,
    params={
        "filter[frequency]": "MONTHLY",
        "filter[reportType]": "SALES",
        "filter[reportSubType]": "SUMMARY",
        "filter[vendorNumber]": "YOUR_VENDOR_NUMBER",
        "filter[reportDate]": "2026-03"
    }
)

if response.status_code == 200:
    decompressed = gzip.GzipFile(fileobj=BytesIO(response.content)).read()
    tsv_data = decompressed.decode('utf-8')
    lines = tsv_data.strip().split('\n')
    header = lines[0].split('\t')
    for line in lines[1:]:
        fields = line.split('\t')
        print(f"{fields[4]}: {fields[7]} units, ${fields[8]} proceeds")

    with open("sales_report.tsv", "w") as f:
        f.write(tsv_data)
```

### Report Parameters

**Frequency:** `DAILY`, `WEEKLY`, `MONTHLY`, `YEARLY`

**Report Types:**
- `SALES` — Unit sales, proceeds, refunds
- `SUBSCRIPTION` — Subscription activity
- `SUBSCRIPTION_EVENT` — Subscription lifecycle events
- `SUBSCRIBER` — Active subscribers
- `SUBSCRIPTION_OFFER_CODE_REDEMPTION` — Offer code usage
- `PRE_ORDER` — Pre-order data
- `INSTALLS` — Install counts
- `FIRST_ANNUAL` — First year activity

**Report Sub-Types:** `SUMMARY`, `DETAILED`, `SUMMARY_INSTALL_TYPE`, `SUMMARY_TERRITORY`, `SUMMARY_CHANNEL`

**Vendor Number:** Find in App Store Connect under Payments and Financial Reports.

**Report Date Format:**
- Daily: `YYYY-MM-DD`
- Weekly: `YYYY-MM-DD` (use Sunday date)
- Monthly: `YYYY-MM`
- Yearly: `YYYY`

## Finance Reports

```python
response = requests.get(
    "https://api.appstoreconnect.apple.com/v1/financeReports",
    headers=headers,
    params={
        "filter[regionCode]": "US",
        "filter[reportDate]": "2026-03",
        "filter[reportType]": "FINANCIAL",
        "filter[vendorNumber]": "YOUR_VENDOR_NUMBER"
    }
)

if response.status_code == 200:
    decompressed = gzip.GzipFile(fileobj=BytesIO(response.content)).read()
    with open("finance_report.tsv", "w") as f:
        f.write(decompressed.decode('utf-8'))
```

Region codes: `US`, `EU`, `GB`, `AU`, `CA`, `JP`, `CN`, etc.

## Common Response Codes

- `200` — Report data returned (gzip)
- `404` — No report available for the requested date (data not yet generated)
- `400` — Invalid filter parameters
