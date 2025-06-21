document.addEventListener("DOMContentLoaded", function () {
  console.log("✅ DOM fully loaded");

  const form = document.getElementById('sqli-form');
  if (!form) {
    console.error("❌ Cannot find form with ID 'sqli-form'");
    return;
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();

    const spinner = document.getElementById('loading-spinner');
    const status = document.getElementById('status');
    const resultsContainer = document.getElementById('result_display');

    spinner.style.display = 'flex';
    status.textContent = 'Starting SQL Injection scan...';
    resultsContainer.innerHTML = '';

    const formData = new FormData(form);

    fetch("{{ url_for('scan_sqli') }}", {  // safer than hardcoding '/scan_sqli'
      method: 'POST',
      body: formData,
    })
      .then(response => response.json())
      .then(data => {
        if (data.error) {
          resultsContainer.innerHTML = `<div class="error">${data.error}</div>`;
        } else {
          let html = `
            <h2>Scan Results</h2>
            <p class="scaned_url_text">Scanned URL: ${data.results.url}</p>
            <p class="found_params_text">Parameters Tested: ${data.results.param_count}</p>
          `;
          if (data.results.vulnerable_params.length > 0) {
            html += `<p id="vul_detected_notification_TRUE"> SQL Injection vulnerabilities found!</p>`;
            data.results.vulnerable_params.forEach(param => {
              html += `
                <div class="vulnerable-param">
                  <p class="param_name_text">Parameter: ${param.name}</p>
                  <p class="param_payload_text">Payload used: ${param.payload}</p>
                </div>
              `;
            });
          } else {
            html += `<p id="vul_detected_notification_FALSE"> No SQL Injection vulnerabilities found.</p>`;
          }
          resultsContainer.innerHTML = html;
        }
      })
      .catch(error => {
        resultsContainer.innerHTML = `<div class="error">Scan failed: ${error.message}</div>`;
      })
      .finally(() => {
        spinner.style.display = 'none';
      });
  });
});
