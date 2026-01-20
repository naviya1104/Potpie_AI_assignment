from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import time
import uuid
import logging
from .schemas import DecisionInput, DecisionOutput, DecisionRequest, DecisionResponse
from .agent import make_decision
from .utils import (
    log_decision_request,
    log_decision_output,
    log_decision_error,
    log_fallback_activation,
    create_safe_fallback_response,
    create_timeout_fallback_response
)

# Initialize FastAPI app
app = FastAPI(
    title="Clarity AI Decision Agent",
    description="AI-powered decision-making system with reasoning and alternatives",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Constants
DECISION_TIMEOUT_SECONDS = 8


@app.get("/")
async def root():
    """Root endpoint - health check"""
    return {
        "status": "healthy",
        "service": "Clarity AI Decision Agent",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "ok",
        "timestamp": time.time()
    }


@app.post("/api/decision", response_model=DecisionResponse)
async def make_ai_decision(decision_request: DecisionRequest) -> DecisionResponse:
    """
    Process a decision request and return AI-generated recommendation
    
    Args:
        decision_request: DecisionRequest containing DecisionInput
        
    Returns:
        DecisionResponse: Contains DecisionOutput with recommendation, reasoning, confidence score, and alternatives
        
    Raises:
        HTTPException: If decision processing fails
    """
    request_id = str(uuid.uuid4())
    start_time = time.time()
    
    try:
        # Log incoming request
        log_decision_request(decision_request.decision_input, request_id)
        
        # Call the decision agent with timeout
        try:
            decision_output = await asyncio.wait_for(
                make_decision(decision_request.decision_input),
                timeout=DECISION_TIMEOUT_SECONDS
            )
        except asyncio.TimeoutError:
            logger.warning(f"Decision processing timeout for request {request_id}")
            log_fallback_activation(
                "Processing timeout exceeded",
                request_id,
                TimeoutError("Decision processing exceeded time limit")
            )
            decision_output = create_timeout_fallback_response()
        
        # Calculate processing time
        processing_time_ms = (time.time() - start_time) * 1000
        
        # Log successful output
        log_decision_output(decision_output, request_id, processing_time_ms)
        
        # Return structured response
        return DecisionResponse(decision_output=decision_output)
        
    except Exception as e:
        logger.error(f"Unhandled error in decision endpoint: {str(e)}", exc_info=True)
        log_decision_error(
            decision_request.decision_input,
            e,
            request_id,
            fallback_used=True
        )
        
        # Return fallback response with error details
        fallback_output = create_safe_fallback_response(
            decision_type=decision_request.decision_input.decision_type,
            context=decision_request.decision_input.context,
            constraint_count=len(decision_request.decision_input.constraints),
            reason=f"System error: {type(e).__name__}"
        )
        
        return DecisionResponse(decision_output=fallback_output)


@app.post("/api/decision/batch")
async def batch_decisions(requests: list[DecisionRequest]):
    """
    Process multiple decision requests in batch
    
    Args:
        requests: List of DecisionRequest objects
        
    Returns:
        List of DecisionResponse objects
    """
    results = []
    
    for request in requests:
        try:
            result = await make_ai_decision(request)
            results.append({"status": "success", "data": result})
        except Exception as e:
            results.append({
                "status": "error",
                "error": str(e),
                "decision_type": request.decision_input.decision_type
            })
    
    return {
        "total": len(requests),
        "successful": sum(1 for r in results if r["status"] == "success"),
        "failed": sum(1 for r in results if r["status"] == "error"),
        "results": results
    }


@app.get("/api/config")
async def get_configuration():
    """
    Get current configuration (without sensitive data)
    
    Returns:
        Configuration information
    """
    return {
        "timeout_seconds": DECISION_TIMEOUT_SECONDS,
        "model": "OpenRouter",
        "features": [
            "Decision recommendations",
            "Reasoning chains",
            "Confidence scores",
            "Alternative options",
            "Fallback handling",
            "Batch processing"
        ]
    }


if __name__ == "__main__":
    import uvicorn
    
    # Run with: python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
