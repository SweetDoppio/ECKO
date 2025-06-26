const observeElementOnScreen = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('in-viewport');
            entry.target.classList.add('visible');
            observeElementOnScreen.unobserve(entry.target);
        } else {
            entry.target.classList.remove('in-viewport');
        }
    });
}, {
    root: null,
    rootMargin: '0px',
    threshold: 0.30
});

document.querySelectorAll('.animate-on-scroll').forEach(element => {
    observeElementOnScreen.observe(element);
});

// Scroll behavior
setTimeout(() => {
    if (window.location.hash !== '#top') {
        const docHeight = document.body.scrollHeight;
        window.scrollTo({
            top: docHeight / 2,
            behavior: 'smooth'
        });
    } else {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
}, 100);
