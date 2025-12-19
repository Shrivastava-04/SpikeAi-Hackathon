from app.agents.analytics_agent import AnalyticsAgent
import os

Property_ID = os.getenv("GA4_PROPERTY_ID")


agent = AnalyticsAgent()
result = agent.run_basic_report(Property_ID)

print(result)