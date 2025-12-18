from app.agents.seo_agent import SEOAgent


agent = SEOAgent()

sheets = agent.list_worksheets()

print("Available Worksheets:")
for s in sheets:
    print(f"- {s}")