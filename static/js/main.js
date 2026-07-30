// MarkMate Dynamic UI & Interactive Utilities

document.addEventListener('DOMContentLoaded', function () {
    // 1. Auto dismiss flash alerts after 4 seconds
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            try {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            } catch (e) {}
        }, 4000);
    });

    // 2. Mobile Sidebar Toggle
    const sidebarToggleBtn = document.getElementById('sidebarToggle');
    const sidebar = document.getElementById('sidebar');
    if (sidebarToggleBtn && sidebar) {
        sidebarToggleBtn.addEventListener('click', function () {
            sidebar.classList.toggle('show');
        });
    }

    // 3. Animated Number Counter for Dashboard Metrics
    const counters = document.querySelectorAll('.counter-value');
    counters.forEach(counter => {
        const targetText = counter.innerText.trim();
        const targetVal = parseFloat(targetText.replace(/[^0-9.]/g, ''));
        const hasPercent = targetText.includes('%');
        
        if (!isNaN(targetVal) && targetVal > 0) {
            let current = 0;
            const duration = 1000; // ms
            const stepTime = 20;
            const steps = duration / stepTime;
            const increment = targetVal / steps;

            const timer = setInterval(() => {
                current += increment;
                if (current >= targetVal) {
                    current = targetVal;
                    clearInterval(timer);
                }
                if (Number.isInteger(targetVal)) {
                    counter.innerText = Math.round(current) + (hasPercent ? '%' : '');
                } else {
                    counter.innerText = current.toFixed(1) + (hasPercent ? '%' : '');
                }
            }, stepTime);
        }
    });

    // 4. Live Clock Widget (if clock element exists)
    const clockElem = document.getElementById('liveClock');
    if (clockElem) {
        const updateClock = () => {
            const now = new Date();
            clockElem.innerText = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
        };
        updateClock();
        setInterval(updateClock, 1000);
    }
});
