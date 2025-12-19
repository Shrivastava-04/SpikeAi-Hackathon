from pydantic import BaseModel
from typing import Literal

class SEOExecutionPlan(BaseModel):
    worksheet: Literal[
        "internal_all",
        "accessibility_all",
        "response_codes_all"
    ]
    analysis_type: Literal[
        "indexability",
        "accessibility",
        "response_codes"
    ]
