document.addEventListener('DOMContentLoaded', () => {
  const modal = document.getElementById('vuln-modal');
  const titleElem = document.getElementById('vuln-modal-title');
  const contentElem = document.getElementById('vuln-modal-content');
  const closeBtn = document.getElementById('close-vuln-modal');

  document.querySelectorAll('.open-vuln-popup').forEach(button => {
    button.addEventListener('click', () => {
      const title = button.getAttribute('data-title');
      const content = button.getAttribute('data-content');

      titleElem.textContent = title;
      contentElem.innerHTML = content;
      modal.style.display = 'block';
    });
  });

  closeBtn.addEventListener('click', () => {
    modal.style.display = 'none';
    contentElem.innerHTML = '';
  });

  window.addEventListener('click', event => {
    if (event.target === modal) {
      modal.style.display = 'none';
      contentElem.innerHTML = '';
    }
  });
});
