from app.agents.seo_agent import SEOAgent

agent = SEOAgent()

df = agent.load_worksheet("internal_all")
results = agent.analyze_indexability(df)
explanation = agent.explain_indexability(results)

print("Indexability Analysis:")
for k, v in results.items():
    print(f"{k}: {v}")

print("\nExplanation:")
print(explanation)
