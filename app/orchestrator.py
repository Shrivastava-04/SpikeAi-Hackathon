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
            
        # SEO Queries            
        try:
            seo_plan = self.llm_client.generate_seo_plan(query)

            df = self.seo_agent.load_worksheet(seo_plan.worksheet)

            if seo_plan.analysis_type == "indexability":
                results = self.seo_agent.analyze_indexability(df)
                summary = self.seo_agent.explain_indexability(results)

            elif seo_plan.analysis_type == "accessibility":
                results = self.seo_agent.analyze_accessibility(df)
                summary = self.seo_agent.explain_accessibility(results)

            elif seo_plan.analysis_type == "response_codes":
                results = self.seo_agent.analyze_response_codes(df)
                summary = self.seo_agent.explain_response_codes(results)

            return {
                "agent": f"seo_{seo_plan.analysis_type}",
                "results": results,
                "summary": summary
            }

        except Exception as e:
            return {
                "error": "Failed to process SEO query",
                "details": str(e)
            }
        return {
            "error": "Unable to determine query intent",
            "hint": "Try asking about GA4 analytics, accessibility, or response codes"
        }


