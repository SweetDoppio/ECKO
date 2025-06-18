document.addEventListener('DOMContentLoaded', function() {
  const navbar = document.getElementById('base-header-container');
  
  window.addEventListener('scroll', function() {
    if (window.scrollY > 50) {
      navbar.classList.add('scroll-state');
    } else {
      navbar.classList.remove('scroll-state');
    }
  })});


setTimeout(() =>{
  const flashMessage = document.querySelector('warning_message_container')
  if (flashMessage){
    flashMessage.display.style = 'none'};
}, 4000)