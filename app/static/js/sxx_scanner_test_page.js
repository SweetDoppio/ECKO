document.querySelector('form').addEventListener('submit', function(e) {
    //event listener will see if url form gets  submitted with valid url
  e.preventDefault(); // stop the form from refreshing page
  const spinner = document.getElementById('loading-spinner');
  const status = document.getElementById('status');
  const resultsContainer = document.getElementById('result_display');
  
  //will show the loading element, while clearing any previous results.
  spinner.style.display = 'flex';
  status.textContent = 'Starting scan...';
  resultsContainer.innerHTML = '';
  
  fetch('/scan', {
    method: 'POST',
    body: new FormData(this)
  })
  .then(response => response.json())
  .then(data => {
    if (data.error) {
      resultsContainer.innerHTML = `<div class="error">${data.error}</div>`;
    } else {
        
      let html = `
        <h2>Scan Results</h2>
        <p class="scaned_url_text">Scanned URL: ${data.results.url}</p>
        <p class="found_forms_text">Forms Found: ${data.results.form_count}</p>
      `;
      
      if (data.results.vulnerable_forms.length > 0) {
        html += `<p id="vul_detected_notification_TRUE">XSS vulnerabilities found!!</p>`;
        data.results.vulnerable_forms.forEach(form => {
          html += `
            <div class="vulnerable-form">
              <p class="form_action_text">Action: ${form.action}</p>
              <p class="form_method_text">Method: ${form.details.method}</p>
            </div>
          `;
        });
      } else {
        html += `<p id="vul_detected_notification_FALSE">No vulnerabilities found</p>`;
      }
      
      resultsContainer.innerHTML = html;
    }
  })
  .catch(error => {
    resultsContainer.innerHTML = `<div class="error">Scan failed!: ${error.message}</div>`;
  })
  .finally(() => {
    spinner.style.display = 'none';
  });
});