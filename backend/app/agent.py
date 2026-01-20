import logging
from pydantic_ai import Agent, ModelRetry
from pydantic import ValidationError

from app.schemas import DecisionInput, DecisionOutput
from app.config import MODEL_NAME

logger = logging.getLogger(__name__)

# --------------------------------------------------
# AI Decision Agent
# --------------------------------------------------

decision_agent = Agent(
    MODEL_NAME,
    system_prompt="""
You are a practical AI decision assistant.

Your job is to HELP the user make a decision, not to refuse.

Rules you MUST follow:
- Always give ONE clear recommendation
- Even if context is limited, make reasonable assumptions
- NEVER say "insufficient context" or ask for more details
- Be specific, actionable, and realistic
- Do not give generic corporate answers

Output format MUST strictly match:
- recommendation: short and direct
- reasoning: 3–5 bullet points
- confidence_score: number between 0 and 1
- alternative_option: one realistic alternative
"""
)

# --------------------------------------------------
# Main decision function
# --------------------------------------------------

async def make_decision(decision_input: DecisionInput) -> DecisionOutput:
    try:
        # Run agent
        result = await decision_agent.run(decision_input.model_dump())

        # pydantic-ai returns structured output directly
        if isinstance(result.output, DecisionOutput):
            return result.output

        # If model returns raw dict
        if isinstance(result.output, dict):
            return DecisionOutput(**result.output)

        # If model returns text (fallback parsing)
        return DecisionOutput(
            recommendation=str(result.output),
            reasoning=[
                "Generated based on common scenarios",
                "Assumptions were made due to limited input",
                "Recommendation favors practical outcomes"
            ],
            confidence_score=0.6,
            alternative_option="Consider revisiting the decision with more constraints"
        )

    except (ModelRetry, ValidationError) as e:
        logger.warning(f"Agent failed, fallback used: {e}")
        return _fallback(decision_input)

    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        return _fallback(decision_input)

# --------------------------------------------------
# Safe fallback (ONLY if model truly fails)
# --------------------------------------------------

def _fallback(decision_input: DecisionInput) -> DecisionOutput:
    return DecisionOutput(
        recommendation="Focus on the option that builds long-term fundamentals first.",
        reasoning=[
            "Foundational skills create flexibility later",
            "This approach minimizes risk under uncertainty",
            "It aligns with typical early-stage decision paths"
        ],
        confidence_score=0.45,
        alternative_option="Split time between both options in small, focused blocks"
    )
