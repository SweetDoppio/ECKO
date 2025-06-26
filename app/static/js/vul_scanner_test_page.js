// Wait until DOM is fully loaded
document.addEventListener("DOMContentLoaded", function () {


  // FOr radat nodes
  const ImNodingSoHard = document.querySelectorAll('.radar-node');
  ImNodingSoHard.forEach(node => {
  node.classList.add('radar-node-hidden')
  });

  ImNodingSoHard.forEach((node, index) => {
    setTimeout(() => {
      node.classList.remove('radar-node-hidden');
      node.classList.add('radar-node-flash');
      
      // Continuous flashing
      setInterval(() => {
        node.classList.toggle('radar-node-flash');
      }, 1500);
    },index * 100); 
  });

  //set display of radar none here
  const spinner = document.querySelector('#loading-spinner');
  spinner.style.display = 'none';

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


  // Activate when use submits url 
  form.addEventListener('submit', function (e) {
    e.preventDefault();

    let resultsContainer = document.getElementById('result_display');

    if (!resultsContainer) {
      resultsContainer = document.createElement('div');
      resultsContainer.id = 'result_display';
      document.getElementById('scan-container').appendChild(resultsContainer);
    }

    // Show loading spinner
    scanButton.disabled = true;

    scanButton.textContent = 'Hang on a sec...'
    spinner.classList.add('scanner-on');
    spinner.style.display = 'flex';
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

        //sql injectio??
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

        //HTTP Scan
          html += `<h3>🔒 HTTPS Security Check</h3>
            <p>URL tested: ${res.url}</p>`;

          if (res.is_https) {
            html += `<p class="safe-text">✅ Secure - This site uses HTTPS</p>`;
          } else {
            if (res.redirects_to_https) {
              html += `<p class="safe-text">✅ Secure - Site redirects to HTTPS</p>`;
            } else if (res.security_issues && res.security_issues.length > 0) {
              html += `<p class="warning-text">⚠️ HTTP Security Issues Detected!</p>
                <div class="vulnerable-box">`;
              res.security_issues.forEach((issue, i, arr) => {
                html += `<p><strong>Issue:</strong> ${issue}</p>
                  ${i !== arr.length - 1 ? '<hr>' : ''}`;
              });
              html += `</div>`;
            } else {
              html += `<p class="warning-text">⚠️ Site does not use HTTPS</p>`;
            }
          }

    
        resultsContainer.innerHTML = html;
                resultsContainer.style.display = 'block'; // Show results container
      }).catch(err => {
        resultsContainer.innerHTML = `<div class="error">❌ Scan failed: ${err.message}</div>`;
          resultsContainer.style.display = 'block';
      }).finally(() => {
          spinner.style.display = 'none';
            scanButton.disabled = false;

      });
  });
});

function centerElement(element) {
    const rect = element.getBoundingClientRect();
    const elementTop = rect.top + window.scrollY;
    const elementHeight = rect.height;
    
    // Calculate center position
    const viewportHeight = window.innerHeight;
    const scrollTo = elementTop - (viewportHeight / 2) + (elementHeight / 2);
    
    // Scroll to that position
    window.scrollTo({
        top: scrollTo,
        behavior: 'smooth' // Optional smooth scrolling
    });
}

const myElement = document.getElementById('scan-container');
centerElement(myElement);