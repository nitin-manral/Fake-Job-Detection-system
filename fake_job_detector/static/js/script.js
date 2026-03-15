document.addEventListener('DOMContentLoaded', function() {
    // Active sidebar link
    const currentPath = window.location.pathname;
    document.querySelectorAll('#sidebar a').forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });

    // Form submission with loading spinner
    const analyzeForm = document.querySelector('form[method="POST"]');
    if (analyzeForm && analyzeForm.querySelector('textarea[name="job_description"]')) {
        analyzeForm.addEventListener('submit', function(e) {
            const submitBtn = this.querySelector('button[type="submit"]');
            const spinner = document.getElementById('loading-spinner');
            
            if (submitBtn && spinner) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Analyzing...';
                spinner.style.display = 'block';
            }
        });
    }

    // Smooth scroll
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });
});
