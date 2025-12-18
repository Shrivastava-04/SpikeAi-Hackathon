from app.agents.analytics_agent import AnalyticsAgent

Property_ID = "<Your_GA4_PROPERTY_ID>"


agent = AnalyticsAgent()
result = agent.run_basic_report(Property_ID)

print(result)