from pydantic import BaseModel, Field
from typing import List, Optional


class DecisionInput(BaseModel):
    """Input schema for AI decision-making system"""
    decision_type: str = Field(..., description="Type of decision to be made")
    context: str = Field(..., description="Contextual information for the decision")
    constraints: List[str] = Field(default_factory=list, description="Constraints that must be considered")
    preferences: dict = Field(default_factory=dict, description="User preferences for the decision")


class DecisionOutput(BaseModel):
    """Output schema for AI decision-making system"""
    recommendation: str = Field(..., description="Primary recommendation from the AI")
    reasoning: List[str] = Field(..., description="List of reasoning steps that led to the recommendation")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Confidence score between 0 and 1")
    alternative_option: Optional[str] = Field(None, description="Alternative option if primary recommendation is not suitable")


class DecisionRequest(BaseModel):
    """Full decision request combining input data"""
    decision_input: DecisionInput


class DecisionResponse(BaseModel):
    """Full decision response combining output data"""
    decision_output: DecisionOutput
