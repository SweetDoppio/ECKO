document.addEventListener('DOMContentLoaded', function() {
    const elements = document.querySelectorAll('h1');
    elements.forEach(element => {
        element.classList.add('about-us-text');
    });
});

// const observeElementOnScreen = new IntersectionObserver((entries) => {
//     entries.forEach(entry => {
//         if(entry.isIntersecting){
//             entry.target.classList.add('in-viewport');
//             entry.target.classList.add('animation-stop');
//         }  else {
//             entry.target.classList.remove('in-viewport');
//         }
//     })
// }, {
//     root: null,
//     rootMargin: '0px', 
//     threshold: 0.30 
// });

// document.querySelectorAll('.animate-on-scroll').forEach(queryElement =>{
//     observeElementOnScreen.observe(queryElement);
// })  Dont really,need this code but just in case.