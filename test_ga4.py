import os
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
)
from google.oauth2 import service_account

# 👉 PASTE YOUR GA4 PROPERTY ID HERE (numbers only)
PROPERTY_ID = os.getenv("GA4_PROPERTY_ID")

# Load credentials from credentials.json
credentials = service_account.Credentials.from_service_account_file(
    "credentials.json"
)

# Create GA4 client
client = BetaAnalyticsDataClient(credentials=credentials)

# Build a simple GA4 report request
request = RunReportRequest(
    property=f"properties/{PROPERTY_ID}",
    dimensions=[Dimension(name="date")],
    metrics=[Metric(name="activeUsers")],
    date_ranges=[DateRange(start_date="7daysAgo", end_date="today")],
)

# Execute the report
response = client.run_report(request)

print("✅ GA4 API call successful")
print(response)
