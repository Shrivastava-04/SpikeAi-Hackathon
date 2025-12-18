from app.agents.seo_agent import SEOAgent

agent = SEOAgent()

df = agent.load_worksheet("response_codes_all")
results = agent.analyze_response_codes(df)
explanation = agent.explain_response_codes(results)

print("Response Codes Analysis:")
for k, v in results.items():
    print(f"{k}: {v}")

print("\nExplanation:")
print(explanation)
