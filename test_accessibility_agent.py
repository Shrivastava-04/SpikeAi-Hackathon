from app.agents.seo_agent import SEOAgent

agent = SEOAgent()

df = agent.load_worksheet("accessibility_all")
results = agent.analyze_wcag_violations(df)
explanation = agent.explain_wcag_results(results)

print("WCAG Results:")
for k, v in results.items():
    print(f"{k}: {v}")

print("\nExplanation:")
print(explanation)
