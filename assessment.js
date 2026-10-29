// Career Assessment Interactive Questionnaire Helper

document.addEventListener('DOMContentLoaded', () => {
    const assessmentForm = document.getElementById('assessmentForm');
    if (!assessmentForm) return;

    const radioInputs = assessmentForm.querySelectorAll('input[type="radio"]');
    const totalQuestions = document.querySelectorAll('.question-block').length;
    const progressFill = document.getElementById('assessmentProgressFill');
    const progressText = document.getElementById('assessmentProgressText');

    function updateProgress() {
        const answeredQuestions = new Set();
        radioInputs.forEach(input => {
            if (input.checked) {
                answeredQuestions.add(input.name);
                // Highlight selected card styling
                const cardLabel = input.closest('.option-card');
                if (cardLabel) {
                    cardLabel.parentElement.querySelectorAll('.option-card').forEach(c => c.classList.remove('selected'));
                    cardLabel.classList.add('selected');
                }
            }
        });

        const answeredCount = answeredQuestions.size;
        const percentage = totalQuestions > 0 ? Math.round((answeredCount / totalQuestions) * 100) : 0;

        if (progressFill) progressFill.style.width = `${percentage}%`;
        if (progressText) progressText.textContent = `${answeredCount} of ${totalQuestions} Questions Completed (${percentage}%)`;
    }

    radioInputs.forEach(input => {
        input.addEventListener('change', updateProgress);
    });

    // Run on initial load
    updateProgress();
});
