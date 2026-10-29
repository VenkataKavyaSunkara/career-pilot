// Jobs Search & Filter Interactions

document.addEventListener('DOMContentLoaded', () => {
    const resetBtn = document.getElementById('resetFiltersBtn');
    if (resetBtn) {
        resetBtn.addEventListener('click', (e) => {
            e.preventDefault();
            window.location.href = window.location.pathname;
        });
    }

    // Auto-submit filter on select change
    const filterSelects = document.querySelectorAll('.filter-select');
    filterSelects.forEach(sel => {
        sel.addEventListener('change', () => {
            const form = sel.closest('form');
            if (form) form.submit();
        });
    });
});
