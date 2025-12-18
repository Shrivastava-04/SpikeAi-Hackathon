# Allowed GA4 fields (SAFE LIST)

ALLOWED_METRICS = {
    "activeUsers",
    "sessions",
    "screenPageViews",
    "eventCount"
}

ALLOWED_DIMENSIONS = {
    "date",
    "pagePath",
    "country",
    "deviceCategory",
    "sessionSource"
}


class GA4QueryPlan:
    def __init__(
        self,
        metrics: list[str],
        dimensions: list[str],
        start_date: str,
        end_date: str
    ):
        self.metrics = metrics
        self.dimensions = dimensions
        self.start_date = start_date
        self.end_date = end_date

    def validate(self):
        for m in self.metrics:
            if m not in ALLOWED_METRICS:
                raise ValueError(f"Metric '{m}' is not allowed")

        for d in self.dimensions:
            if d not in ALLOWED_DIMENSIONS:
                raise ValueError(f"Dimension '{d}' is not allowed")
