document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('prediction-form');
    const resultContainer = document.getElementById('result-container');
    const loading = document.getElementById('loading');
    const result = document.getElementById('result');
    const errorDiv = document.getElementById('error');
    const resultStatus = document.getElementById('result-status');
    const resultProb = document.getElementById('result-prob');
    const submitBtn = document.getElementById('submit-btn');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // UI States
        submitBtn.disabled = true;
        resultContainer.classList.remove('hidden');
        loading.classList.remove('hidden');
        result.classList.add('hidden');
        errorDiv.classList.add('hidden');

        // Gather data
        const formData = new FormData(form);
        const data = {
            fo: parseFloat(formData.get('fo')),
            fhi: parseFloat(formData.get('fhi')),
            flo: parseFloat(formData.get('flo')),
            jitter_percent: parseFloat(formData.get('jitter_percent')),
            shimmer: parseFloat(formData.get('shimmer')),
            hnr: parseFloat(formData.get('hnr'))
        };

        try {
            const response = await fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });

            if (!response.ok) {
                const errData = await response.json();
                throw new Error(errData.detail || 'Failed to analyze data');
            }

            const resultData = await response.json();
            
            // Update UI
            loading.classList.add('hidden');
            result.classList.remove('hidden');
            
            resultStatus.textContent = resultData.status;
            resultProb.textContent = resultData.risk_probability;

            // Apply classes based on status
            if (resultData.prediction === 1) {
                result.className = 'status-risk';
            } else {
                result.className = 'status-healthy';
            }

        } catch (error) {
            loading.classList.add('hidden');
            errorDiv.classList.remove('hidden');
            errorDiv.textContent = `Error: ${error.message}`;
        } finally {
            submitBtn.disabled = false;
        }
    });
});
