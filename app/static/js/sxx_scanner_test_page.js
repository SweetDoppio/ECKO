document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById('sqli-form');
  if (!form) return;

  form.addEventListener('submit', function (e) {
    e.preventDefault();

    const spinner = document.getElementById('loading-spinner');
    const status = document.getElementById('status');
    const resultsContainer = document.getElementById('result_display');

    spinner.style.display = 'flex';
    status.textContent = 'Starting vulnerability scan...';
    resultsContainer.innerHTML = '';

    fetch('/scan_sqli', {
      method: 'POST',
      body: new FormData(form)
    })
      .then(res => res.json())
      .then(data => {
        if (data.error) {
          resultsContainer.innerHTML = `<div class="error">${data.error}</div>`;
          return;
        }

        const res = data.results;
        let html = `<h2>🔎 Scan Results</h2><p class="scaned_url_text">URL: ${res.url}</p>`;

        // === SQL Injection Results ===
        html += `<h3>🧬 SQL Injection</h3>`;
        html += `<p class="found_params_text">Parameters Tested: ${res.sqli_results.param_count}</p>`;
        if (res.sqli_results.vulnerable_params.length > 0) {
          html += `<p class="vul_detected_true">⚠️ SQLi vulnerabilities detected!</p><ul>`;
          res.sqli_results.vulnerable_params.forEach(v => {
            html += `<li><b>${v.name}</b>: ${v.payload}</li>`;
          });
          html += `</ul>`;
        } else {
          html += `<p class="vul_detected_false">✅ No SQLi vulnerabilities found.</p>`;
        }

        // === XSS Results ===
        html += `<h3>🧪 Cross-Site Scripting (XSS)</h3>`;
        html += `<p class="found_forms_text">Forms Detected: ${res.xss_results.form_count}</p>`;
        if (res.xss_results.vulnerable_forms.length > 0) {
          html += `<p class="vul_detected_true">⚠️ XSS vulnerabilities detected!</p><ul>`;
          res.xss_results.vulnerable_forms.forEach(form => {
            html += `
              <li>
                <b>Form Action:</b> ${form.action}<br/>
                <b>Method:</b> ${form.details.method}
              </li>
            `;
          });
          html += `</ul>`;
        } else {
          html += `<p class="vul_detected_false">✅ No XSS vulnerabilities found.</p>`;
        }

        resultsContainer.innerHTML = html;
      })
      .catch(err => {
        resultsContainer.innerHTML = `<div class="error">❌ Scan failed: ${err.message}</div>`;
      })
      .finally(() => {
        spinner.style.display = 'none';
      });
  });
});
