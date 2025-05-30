const observeElementOnScreen = new IntersectionObserver((entries) => {
    entries.forEach(entry =>{ //Create array for 'entries'
        if( entry.isIntersecting){
            entry.target.classList.add('in-viewport')
            entry.target.classList.add('animation-stop') 
            observeElementOnScreen.unobserve(entry.target); //remove from observer obj  
        } else {
            entry.target.classList.remove('in-viewport')
        }
    });
}, {
    root: null, //observes against viewport
    rootMargin: '0px', 
    threshold: 0.30 /* percentage value of when the element should be shown before triggering event*/

});

document.querySelectorAll('.animate-on-scroll').forEach(element => {
    observeElementOnScreen.observe(element)
})


Array.from(document.getElementsByTagName('h4')).forEach(element => {
    element.classList.add('help_text');
});


