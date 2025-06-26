document.addEventListener('DOMContentLoaded', function() {

  const navbar = document.getElementById('base-header-container');
  const batImage = document.querySelector('#batHoleLogo');
  window.addEventListener('scroll', function() {
    if (window.scrollY > 50) {
      navbar.classList.add('scroll-state');
      batImage.src = batImage.dataset.alternateSrc; 



    } else {
      navbar.classList.remove('scroll-state');
      batImage.src = batImage.dataset.src; 

    }
  })});


setTimeout(() =>{
  const flashMessage = document.querySelector('warning_message_container')
  if (flashMessage){
    flashMessage.display.style = 'none'};
}, 4000)