from app.agents.analytics_agent import AnalyticsAgent
from app.agents.ga4_schema import GA4QueryPlan
from app.agents.llm_client import LLMClient
from app.agents.seo_agent import SEOAgent

class Orchestrator:
    def __init__(self):
        self.analytics_agent = AnalyticsAgent()
        self.llm_client = LLMClient()
        self.seo_agent = SEOAgent()

    def handle_query(self, query: str, property_id: str | None):
        q = query.lower()
        #LLMClient to generate GA4QueryPlan from user query

        # GA4 Analytics (highest priority)

        if property_id:
            try:
                plan_dict = self.llm_client.generate_ga4_plan(query)

                start_date = (
                    plan_dict.get("start_date")
                    or plan_dict.get("startDate")
                )

                end_date = (
                    plan_dict.get("end_date")
                    or plan_dict.get("endDate")
                )

                if not start_date or not end_date:
                    raise ValueError("start_date / end_date missing in LLM response")

                plan = GA4QueryPlan(
                    metrics=plan_dict["metrics"],
                    dimensions=plan_dict["dimensions"],
                    start_date=start_date,
                    end_date=end_date
                )   
                
                return self.analytics_agent.run_report(property_id, plan)
            except Exception as e:
                return {
                    "error": "Failed to process analytics query.",
                    "details": str(e)
                }
        
        # SEO: Accessibility (WCAG)

        if any(keyword in q for keyword in [ "accessibility", "wcag", "a11y"]):
            try:
                df = self.seo_agent.load_worksheet("accessibility_all")
                results = self.seo_agent.analyze_wcag_violations(df)
                explaination = self.seo_agent.explain_wcag_results(results)

                return {
                    "agent": "SEOAgent",
                    "results": results,
                    "explaination": explaination
                }
            except Exception as e:
                return {
                    "error": "Failed to process SEO query.",
                    "details": str(e)
                }

        # SEO: Response Codes / Crawl Health

        if any(k in q for k in ["status", "response", "crawl", "redirect", "4xx", "5xx"]):
            try:
                df = self.seo_agent.load_worksheet("response_codes_all")
                results = self.seo_agent.analyze_response_codes(df)
                explanation = self.seo_agent.explain_response_codes(results)

                return {
                    "agent": "seo_response_codes",
                    "results": results,
                    "summary": explanation
                }
            except Exception as e:
                return {
                    "error": "Failed to process response codes SEO query",
                    "details": str(e)
                }

        # ---------------------------
        # Fallback
        # ---------------------------
        return {
            "error": "Unable to determine query intent",
            "hint": "Try asking about GA4 analytics, accessibility, or response codes"
        }
    

