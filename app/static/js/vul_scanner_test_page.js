// Wait until DOM is fully loaded
document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById('sqli-form');
  const scanButton = document.querySelector('.scanner-button');
  const urlBar = document.querySelector('form input[type="url"]')

  urlBar.addEventListener('mouseover', ()=> {
    urlBar.classList.add('mouseover');
  })
  urlBar.addEventListener("mouseout", ()=>{
        urlBar.classList.remove('mouseover');
  });

  scanButton.addEventListener('mouseover', ()=> {
    scanButton.classList.add('radar-pulse');
  })
  scanButton.addEventListener("mouseout", ()=>{
        scanButton.classList.remove('radar-pulse');
  });
  form.addEventListener('submit', function (e) {
    e.preventDefault();


    const spinner = document.getElementById('loading-spinner');
    
    let resultsContainer = document.getElementById('result_display');

    if (!resultsContainer) {
      resultsContainer = document.createElement('div');
      resultsContainer.id = 'result_display';
      document.getElementById('scan-container').appendChild(resultsContainer);
    }

    // Show loading spinner
    scanButton.disabled = true;

    scanButton.textContent = 'Hang on a sec...'
    // spinner.style.display = 'flex';
    resultsContainer.innerHTML = '';
    resultsContainer.style.display = 'block';

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
        let html = `
          <div class="centered">
            <h2>🔍 Scan Results</h2>
            <p class="scaned_url_text">URL: ${res.url}</p>
          </div>

          <div class="vul-results-left">
            <h3> SQL Injection</h3>
            <p>Parameters Tested: ${res.sqli_results.param_count}</p>
        `;

        if (res.sqli_results.vulnerable_params.length > 0) {
          html += `<p class="warning-text">⚠️ SQLi vulnerabilities detected!</p>`;
          html += `<div class="vulnerable-box">`;
          res.sqli_results.vulnerable_params.forEach((v, i, arr) => {
            html += `
              <p><strong>Parameter:</strong> ${v.name}</p>
              <p><strong>Payload used:</strong> ${v.payload}</p>
              ${i !== arr.length - 1 ? '<hr>' : ''}
            `;
          });
          html += `</div>`;
        } else {
          html += `<p class="safe-text">✅ No SQLi vulnerabilities found.</p>`;
        }

        scanButton.textContent = 'Here is the result!';


        // XSS section
        html += `
          <h3>🧪 Cross-Site Scripting (XSS)</h3>
          <p>Forms Detected: ${res.xss_results.form_count}</p>
        `;

        if (res.xss_results.vulnerable_forms.length > 0) {
          html += `<p class="warning-text">⚠️ XSS vulnerabilities detected!</p>`;
          html += `<div class="vulnerable-box">`;
          res.xss_results.vulnerable_forms.forEach((form, i, arr) => {
            html += `
              <p><strong>Form Action:</strong> ${form.action}</p>
              <p><strong>Method:</strong> ${form.details.method}</p>
              ${i !== arr.length - 1 ? '<hr>' : ''}
            `;
          });
          html += `</div>`;
        } else {
          html += `<p class="safe-text">✅ No XSS vulnerabilities found.</p>`;
        }


        if (httpIssues.length > 0) {
          html += `<p class="warning-text">⚠️ HTTP Security Issues Detected!</p>`;
          html += `<div class="vulnerable-box">`;
          httpIssues.forEach((issue, i, arr) => {
            html += `
              <p><strong>Issue:</strong> ${issue.security_issues || 'Unknown issue'}</p>
              ${i !== arr.length - 1 ? '<hr>' : ''}
            `;
          });
          html += `</div>`;
        } else {
          html += `<p class="safe-text">✅ No HTTP security issues found.</p>`;
        }

        resultsContainer.innerHTML = html;
                resultsContainer.style.display = 'block'; // Show results container
      })
      .catch(err => {
        resultsContainer.innerHTML = `<div class="error">❌ Scan failed: ${err.message}</div>`;
                resultsContainer.style.display = 'block';
      })
      .finally(() => {
        // spinner.style.display = 'none';
            scanButton.disabled = false;

      });
  });
});