from google.oauth2 import service_account
from googleapiclient.discovery import build
import pandas as pd


class SEOAgent:
    def __init__(self):
        self.sheet_id = "1zzf4ax_H2WiTBVrJigGjF2Q3Yz-qy2qMCbAMKvl6VEE"
        self.credentials_file = "credentials.json"

        self.scopes = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

        self.creds = service_account.Credentials.from_service_account_file(
            self.credentials_file,
            scopes=self.scopes
        )

        self.service = build("sheets", "v4", credentials=self.creds)

    
    def list_worksheets(self):
        spreadsheet = self.service.spreadsheets().get(
            spreadsheetId=self.sheet_id
        ).execute()

        sheets = spreadsheet.get("sheets", [])
        sheet_names = [
            sheet["properties"]["title"]
            for sheet in sheets
        ]

        return sheet_names


    def load_worksheet(self, sheet_name: str) -> pd.DataFrame:
        result = self.service.spreadsheets().values().get(
            spreadsheetId=self.sheet_id,
            range=sheet_name
        ).execute()

        values = result.get("values", [])

        if not values or len(values) < 2:
            raise ValueError(f"No data found in worksheet: {sheet_name}")

        headers = values[0]
        rows = values[1:]

        normalized_rows = []
        num_cols = len(headers)

        for row in rows:
            if len(row) < num_cols:
                # Pad missing cells with empty string
                row = row + [""] * (num_cols - len(row))
            elif len(row) > num_cols:
                # Trim extra cells (rare, but safe)
                row = row[:num_cols]

            normalized_rows.append(row)

        return pd.DataFrame(normalized_rows, columns=headers)

    def analyze_wcag_violations(self, df):

        results = {}
        total_urls = len(df)

        results["total_urls"] = total_urls

        # Detect WCAG columns dynamically
        wcag_columns = {
            "wcag_2_0_a": None,
            "wcag_2_0_aa": None,
            "wcag_2_1_aa": None,
            "wcag_2_2_aa": None,
        }

        for col in df.columns:
            col_lower = col.lower()
            if "wcag 2.0 a" in col_lower:
                wcag_columns["wcag_2_0_a"] = col
            elif "wcag 2.0 aa" in col_lower:
                wcag_columns["wcag_2_0_aa"] = col
            elif "wcag 2.1 aa" in col_lower:
                wcag_columns["wcag_2_1_aa"] = col
            elif "wcag 2.2 aa" in col_lower:
                wcag_columns["wcag_2_2_aa"] = col

        # Count violations
        for key, col in wcag_columns.items():
            if col:
                violating = df[df[col].notna() & (df[col] != "0")]
                results[f"{key}_violations"] = len(violating)
                results[f"{key}_percentage"] = round(
                    (len(violating) / total_urls) * 100, 2
                )
            else:
                results[f"{key}_violations"] = None
                results[f"{key}_percentage"] = None

        return results

    def explain_wcag_results(self, results):
        explanations = []

        if results.get("wcag_2_2_aa_violations") is not None:
            count = results["wcag_2_2_aa_violations"]
            pct = results["wcag_2_2_aa_percentage"]

            if count > 0:
                explanations.append(
                    f"{count} URLs ({pct}%) violate WCAG 2.2 AA, "
                    "which may pose accessibility and legal compliance risks."
                )
            else:
                explanations.append(
                    "No WCAG 2.2 AA violations detected, indicating good accessibility compliance."
                )

        return " ".join(explanations)

    def analyze_response_codes(self, df):
        results = {}

        total_urls = len(df)
        results["total_urls"] = total_urls

        # Detect columns safely
        status_code_col = None
        status_text_col = None

        for col in df.columns:
            if col.lower() == "status code":
                status_code_col = col
            if col.lower() == "status":
                status_text_col = col

        if not status_code_col:
            return {"error": "Status Code column not found"}

        # Convert status code to numeric safely
        df[status_code_col] = pd.to_numeric(df[status_code_col], errors="coerce")

        results["ok_200"] = int((df[status_code_col] == 200).sum())
        results["redirect_3xx"] = int(((df[status_code_col] >= 300) & (df[status_code_col] < 400)).sum())
        results["error_4xx"] = int(((df[status_code_col] >= 400) & (df[status_code_col] < 500)).sum())
        results["error_5xx"] = int((df[status_code_col] >= 500).sum())

        # Blocked by robots.txt is represented as status code 0
        results["blocked_by_robots"] = int((df[status_code_col] == 0).sum())

        # Percentages
        for key in ["ok_200", "redirect_3xx", "error_4xx", "error_5xx", "blocked_by_robots"]:
            results[f"{key}_percentage"] = round((results[key] / total_urls) * 100, 2)

        return results

    def explain_response_codes(self, results):
        if "error" in results:
            return results["error"]

        explanation = []

        explanation.append(
            f"{results['ok_200']} URLs ({results['ok_200_percentage']}%) return 200 OK."
        )

        if results["redirect_3xx"] > 0:
            explanation.append(
                f"{results['redirect_3xx']} URLs ({results['redirect_3xx_percentage']}%) are redirects (3xx), which may affect crawl efficiency."
            )

        if results["blocked_by_robots"] > 0:
            explanation.append(
                f"{results['blocked_by_robots']} URLs ({results['blocked_by_robots_percentage']}%) are blocked by robots.txt."
            )

        if results["error_4xx"] > 0:
            explanation.append(
                f"{results['error_4xx']} URLs return 4xx errors, indicating broken or missing pages."
            )

        if results["error_5xx"] > 0:
            explanation.append(
                f"{results['error_5xx']} URLs return 5xx errors, indicating server issues."
            )

        if results["error_4xx"] == 0 and results["error_5xx"] == 0:
            explanation.append(
                "No client or server errors detected, indicating good crawl health."
            )

        return " ".join(explanation)


    def analyze_indexability(self, df):
        results = {}

        total_pages = len(df)
        results["total_pages"] = total_pages

        # Required columns
        status_code_col = "Status Code"
        status_col = "Status"
        meta_robots_col = "Meta Robots 1"
        xrobots_col = "X-Robots-Tag 1"
        canonical_col = "Canonical Link Element 1"
        redirect_col = "Redirect URL"

        for col in [status_code_col, status_col]:
            if col not in df.columns:
                return {"error": f"Required column missing: {col}"}

        # Normalize text columns
        for col in [meta_robots_col, xrobots_col, canonical_col, redirect_col]:
            if col in df.columns:
                df[col] = df[col].fillna("").astype(str).str.lower()

        # Convert status code
        df[status_code_col] = pd.to_numeric(df[status_code_col], errors="coerce")

        indexable_mask = (
            (df[status_code_col] == 200) &
            (~df[status_col].str.contains("blocked", case=False, na=False)) &
            (~df[meta_robots_col].str.contains("noindex", na=False)) &
            (~df[xrobots_col].str.contains("noindex", na=False)) &
            (df[redirect_col] == "") &
            ((df[canonical_col] == "") | (df[canonical_col] == df["Address"]))
        )

        indexable_count = int(indexable_mask.sum())
        non_indexable_count = total_pages - indexable_count

        results["indexable_pages"] = indexable_count
        results["non_indexable_pages"] = non_indexable_count

        if total_pages > 0:
            percentage = round((indexable_count / total_pages) * 100, 2)
        else:
            percentage = 0.0

        results["indexable_percentage"] = percentage

        # SEO health assessment
        if percentage >= 80:
            health = "Good"
        elif percentage >= 50:
            health = "Average"
        else:
            health = "Poor"

        results["technical_seo_health"] = health

        return results


    def explain_indexability(self, results):
        if "error" in results:
            return results["error"]

        return (
            f"{results['indexable_percentage']}% of pages are indexable. "
            f"This indicates {results['technical_seo_health'].lower()} technical SEO health. "
            f"Indexable pages are eligible to appear in search engine results."
        )
