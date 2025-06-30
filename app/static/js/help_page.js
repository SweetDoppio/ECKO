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


