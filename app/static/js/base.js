document.addEventListener('DOMContentLoaded', function() {

  const navbar = document.getElementById('base-header-container');
  const batImage = document.querySelector('#batHoleLogo');
  const textNavBar = document.querySelectorAll('.header-list-text-main');
  const signUpButton = document.querySelector('.header-list-text-sign');

  window.addEventListener('scroll', function() {
    if (window.scrollY > 50) {
      textNavBar.forEach((text)=>{
        text.classList.add('scroll-state');
      })
      navbar.classList.add('scroll-state');
      batImage.src = batImage.dataset.alternateSrc; 
      signUpButton.classList.add('scroll-state');

    } else {
      textNavBar.forEach((text)=>{
        text.classList.remove('scroll-state');
      })
      navbar.classList.remove('scroll-state');

      batImage.src = batImage.dataset.src; 
      signUpButton.classList.remove('scroll-state');

    }
  })});


setTimeout(() =>{
  const flashMessage = document.querySelector('warning_message_container')
  if (flashMessage){
    flashMessage.display.style = 'none'};
}, 4000)