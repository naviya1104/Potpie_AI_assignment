// Configuration
const API_BASE_URL = 'http://localhost:8000';
const DECISION_ENDPOINT = `${API_BASE_URL}/api/decision`;

// DOM Elements
const decisionForm = document.getElementById('decisionForm');
const decisionTypeInput = document.getElementById('decisionType');
const contextInput = document.getElementById('context');
const constraintsInput = document.getElementById('constraints');
const preferencesInput = document.getElementById('preferences');
const submitBtn = document.getElementById('submitBtn');
const resultContainer = document.getElementById('result');
const loadingSpinner = document.getElementById('loading');

// Event Listeners
document.addEventListener('DOMContentLoaded', initializeForm);
submitBtn.addEventListener('click', handleFormSubmit);

/**
 * Initialize the form with default values
 */
function initializeForm() {
    console.log('Initializing decision form...');
    preferencesInput.value = JSON.stringify({}, null, 2);
}

/**
 * Handle form submission
 */
async function handleFormSubmit(event) {
    event.preventDefault();
    
    // Validate form inputs
    if (!validateForm()) {
        return;
    }
    
    // Prepare request data
    const requestData = prepareRequestData();
    
    // Show loading state
    showLoading(true);
    resultContainer.innerHTML = '';
    
    try {
        // Make API call
        const response = await makeDecisionRequest(requestData);
        
        // Display results
        displayDecisionResult(response);
    } catch (error) {
        displayError(error);
    } finally {
        showLoading(false);
    }
}

/**
 * Validate form inputs
 */
function validateForm() {
    const errors = [];
    
    if (!decisionTypeInput.value.trim()) {
        errors.push('Decision type is required');
    }
    
    if (!contextInput.value.trim()) {
        errors.push('Context is required');
    }
    
    if (preferencesInput.value.trim()) {
        try {
            JSON.parse(preferencesInput.value);
        } catch (e) {
            errors.push('Preferences must be valid JSON');
        }
    }
    
    if (errors.length > 0) {
        displayError(new Error(errors.join('\n')));
        return false;
    }
    
    return true;
}

/**
 * Prepare request data from form inputs
 */
function prepareRequestData() {
    const constraints = constraintsInput.value
        .split('\n')
        .map(c => c.trim())
        .filter(c => c.length > 0);
    
    let preferences = {};
    if (preferencesInput.value.trim()) {
        preferences = JSON.parse(preferencesInput.value);
    }
    
    return {
        decision_input: {
            decision_type: decisionTypeInput.value.trim(),
            context: contextInput.value.trim(),
            constraints: constraints,
            preferences: preferences
        }
    };
}

/**
 * Make API request to backend
 */
async function makeDecisionRequest(requestData) {
    const response = await fetch(DECISION_ENDPOINT, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        body: JSON.stringify(requestData)
    });
    
    if (!response.ok) {
        throw new Error(`API request failed: ${response.status} ${response.statusText}`);
    }
    
    return await response.json();
}

/**
 * Display decision result in UI
 */
function displayDecisionResult(responseData) {
    const output = responseData.decision_output || responseData;
    
    const html = `
        <div class="result-card">
            <h3>AI Decision Result</h3>
            
            <div class="result-section">
                <h4>Recommendation</h4>
                <p class="recommendation">${escapeHtml(output.recommendation)}</p>
            </div>
            
            <div class="result-section">
                <h4>Reasoning</h4>
                <ul class="reasoning-list">
                    ${output.reasoning.map(reason => `<li>${escapeHtml(reason)}</li>`).join('')}
                </ul>
            </div>
            
            <div class="result-section metrics">
                <div class="metric">
                    <span class="metric-label">Confidence Score:</span>
                    <span class="metric-value">${(output.confidence_score * 100).toFixed(1)}%</span>
                    <div class="confidence-bar">
                        <div class="confidence-fill" style="width: ${output.confidence_score * 100}%"></div>
                    </div>
                </div>
            </div>
            
            ${output.alternative_option ? `
                <div class="result-section">
                    <h4>Alternative Option</h4>
                    <p class="alternative">${escapeHtml(output.alternative_option)}</p>
                </div>
            ` : ''}
            
            <button class="btn-secondary" onclick="resetForm()">Make Another Decision</button>
        </div>
    `;
    
    resultContainer.innerHTML = html;
    resultContainer.scrollIntoView({ behavior: 'smooth' });
}

/**
 * Display error message in UI
 */
function displayError(error) {
    const errorMessage = error.message || 'An unknown error occurred';
    
    const html = `
        <div class="error-card">
            <h3>Error Processing Decision</h3>
            <p class="error-message">${escapeHtml(errorMessage)}</p>
            <p class="error-hint">Please check your inputs and try again, or contact support if the problem persists.</p>
            <button class="btn-secondary" onclick="resultContainer.innerHTML = ''">Dismiss</button>
        </div>
    `;
    
    resultContainer.innerHTML = html;
    resultContainer.scrollIntoView({ behavior: 'smooth' });
    console.error('Error:', error);
}

/**
 * Show/hide loading spinner
 */
function showLoading(isLoading) {
    if (isLoading) {
        loadingSpinner.style.display = 'block';
        submitBtn.disabled = true;
    } else {
        loadingSpinner.style.display = 'none';
        submitBtn.disabled = false;
    }
}

/**
 * Reset form to initial state
 */
function resetForm() {
    decisionForm.reset();
    resultContainer.innerHTML = '';
    preferencesInput.value = JSON.stringify({}, null, 2);
    decisionTypeInput.focus();
}

/**
 * Escape HTML special characters for safe display
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Export functions for testing
window.DecisionAgent = {
    makeDecision: handleFormSubmit,
    resetForm: resetForm
};
