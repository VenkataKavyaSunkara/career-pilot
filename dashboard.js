// Student Dashboard Interactions

document.addEventListener('DOMContentLoaded', () => {
    // Dynamic greeting based on current hour
    const greetingEl = document.getElementById('timeGreeting');
    if (greetingEl) {
        const hour = new Date().getHours();
        let greeting = "Good day";
        if (hour < 12) greeting = "Good morning";
        else if (hour < 18) greeting = "Good afternoon";
        else greeting = "Good evening";
        greetingEl.textContent = greeting;
    }

    // Animate progress bars on scroll/load
    const progressBars = document.querySelectorAll('.progress-bar-fill');
    progressBars.forEach(bar => {
        const targetWidth = bar.getAttribute('data-width');
        if (targetWidth) {
            setTimeout(() => {
                bar.style.width = targetWidth;
            }, 100);
        }
    });
});
