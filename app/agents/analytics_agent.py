from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
)
from google.oauth2 import service_account
from app.agents.ga4_schema import GA4QueryPlan


class AnalyticsAgent:
    def __init__(self):
        self.credentials = service_account.Credentials.from_service_account_file(
            "credentials.json"
        )
        self.client = BetaAnalyticsDataClient(credentials=self.credentials)

    def run_report(self, property_id: str, plan: GA4QueryPlan):
        # Validate plan before execution
        plan.validate()

        request = RunReportRequest(
            property=f"properties/{property_id}",
            dimensions=[Dimension(name=d) for d in plan.dimensions],
            metrics=[Metric(name=m) for m in plan.metrics],
            date_ranges=[
                DateRange(
                    start_date=plan.start_date,
                    end_date=plan.end_date
                )
            ],
        )

        response = self.client.run_report(request)

        rows = []

        for row in response.rows:
            row_data = {}
            for i, d in enumerate(plan.dimensions):
                row_data[d] = row.dimension_values[i].value
            for i, m in enumerate(plan.metrics):
                row_data[m] = row.metric_values[i].value
            rows.append(row_data)

        if not rows:
            return {
                "data": [],
                "summary": "No data found for the given query parameters. This may indicate low or no traffic."
            }

        return {
            "data": rows,
            "summary": f"Returned {len(rows)} rows for the requested analytics query."
        }
