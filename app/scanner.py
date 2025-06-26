import requests
import time
from flask import flash
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin, urlparse, parse_qs
import validators

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; EKHOScanner/1.0; +https://yourtool.example)"
}

class Scanner:
    def __init__(self, url):
        self.url = url

    #simple method tot check if entered url is a proper url
    def validateUrl(self):
        if not self.url:
            return False
        if not self.url.startswith(('http://', 'https://')):
            flash('URL must start with either "https://" or "http://"')
            return False
        if not validators.url(self.url):
            flash('Invalid URL format!')
            return False
        return True

    
    def getAllForms(self):
        try:
            response = requests.get(self.url, headers=HEADERS, timeout=5)
            response.raise_for_status()
            soup = bs(response.content, 'html.parser')
            return soup.find_all('form')
        except Exception as e:
            flash(f"Error retrieving forms: {e}")
            return []

    def getFormDetails(self, form):
        action = form.attrs.get('action', '').lower()
        method = form.attrs.get('method', 'get').lower()
        inputs = []

        for input_tag in form.find_all('input'):
            input_type = input_tag.attrs.get('type', 'text')
            input_name = input_tag.attrs.get('name')
            inputs.append({'type': input_type, 'name': input_name})

        return {
            "action": action,
            "method": method,
            "inputs": inputs
        }

    
    def submitForm(self, form_details, payload):
        target_url = urljoin(self.url, form_details['action'])
        data = {}

        for input in form_details['inputs']:
            if input['type'] in ['text', 'search']:
                input['value'] = payload
            name = input.get('name')
            value = input.get('value')
            if name and value:
                data[name] = value

        try:
            if form_details['method'] == 'post':
                return requests.post(target_url, data=data, headers=HEADERS, timeout=7)
            else:
                return requests.get(target_url, params=data, headers=HEADERS, timeout=7)
        except Exception as e:
            flash(f"Request error on {target_url}: {e}")
            return None


    ##http method
    def checkhttps(self):
        results = {
            'url': self.url,
            'is_https': False,
            'redirects_to_https': False,
            'security_issues': []
        }
        try:
            # check to see if URL is already HTTPS
            if self.url.startswith('https://'):
                results['is_https'] = True
                return results
          
            if self.url.startswith('http://'):
                response = requests.get(self.url, headers=HEADERS, allow_redirects=True, timeout=5)
                final_url = response.url
                if final_url.startswith('https://'):
                    results['redirects_to_https'] = True
                else:
                    results['security_issues'].append('Site does not redirect to HTTPS')
            return results
            
        except Exception as e:
            results['security_issues'].append(f'Error checking HTTPS: {str(e)}')
            return results
            
    
    def scanXss(self):
        results = {
            'url': self.url,
            'form_count': 0,
            'vulnerable_forms': []
        }
        #list of payloads that will be entered 
        payloads = [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "<svg/onload=alert('XSS')>",
            "'\"><script>alert('XSS')</script>",
            "<script>alert('Hope your site is secure =]')</script>"
        ]

        forms = self.getAllForms()
        results['form_count'] = len(forms)

        for form in forms:
            details = self.getFormDetails(form)
            for payload in payloads:
                response = self.submitForm(details, payload)
                if response and payload in response.text:
                    results['vulnerable_forms'].append({
                        'details': details,
                        'action': urljoin(self.url, details['action'])
                    })
                    break
        return results


    ##SQL METHOD
    def scanSqli(self):
        results = {
            'url': self.url,
            'param_count': 0,
            'vulnerable_params': []
        }

        payloads = [
            "'", "' OR '1'='1", "\" OR \"1\"=\"1", "' OR 1=1--",
            "'; DROP TABLE users--", "' OR SLEEP(3)--"
        ]

        parsed = urlparse(self.url)
        query_params = parse_qs(parsed.query)

        # Case 1: URL-based parameters
        if query_params:
            for param in query_params:
                for payload in payloads:
                    test_params = query_params.copy()
                    test_params[param] = payload
                    query = "&".join([f"{k}={v}" for k, v in test_params.items()])
                    test_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}?{query}"

                    try:
                        start = time.time()
                        response = requests.get(test_url, headers=HEADERS, timeout=10)
                        elapsed = time.time() - start
                        content = response.text.lower()

                        if any(err in content for err in ["sql syntax", "mysql_fetch", "odbc_exec",
                                                          "unclosed quotation mark", "unterminated string", "syntax error"]):
                            results['vulnerable_params'].append({
                                'name': param,
                                'payload': payload
                            })
                            break
                        elif elapsed > 2.5:
                            results['vulnerable_params'].append({
                                'name': param,
                                'payload': payload + " (blind)"
                            })
                            break
                    except Exception as e:
                        flash(f"URL SQLi test error on '{param}': {e}")

        # Case 2: Fform-based injection
        forms = self.getAllForms()
        for form in forms:
            details = self.getFormDetails(form)
            for input in details['inputs']:
                name = input.get('name')
                if not name:
                    continue

                for payload in payloads:
                    data = {name: payload}
                    try:
                        start = time.time()
                        if details['method'] == 'post':
                            response = requests.post(urljoin(self.url, details['action']), data=data, headers=HEADERS, timeout=10)
                        else:
                            response = requests.get(urljoin(self.url, details['action']), params=data, headers=HEADERS, timeout=10)
                        elapsed = time.time() - start
                        content = response.text.lower()

                        if any(err in content for err in ["sql syntax", "mysql_fetch", "odbc_exec",
                                                          "unclosed quotation mark", "unterminated string", "syntax error"]):
                            results['vulnerable_params'].append({
                                'name': name,
                                'payload': payload
                            })
                            break
                        elif elapsed > 2.5:
                            results['vulnerable_params'].append({
                                'name': name,
                                'payload': payload + " (blind)"
                            })
                            break
                    except Exception as e:
                        flash(f"{details['method'].upper()} SQLi test error on '{name}': {e}")

        results['param_count'] = len(results['vulnerable_params'])
        return results

    def scanBoth(self):
        return {
            'url': self.url,
            'sqli_results': self.scanSqli(),
            'xss_results': self.scanXss(),
            'http_results' : self.checkhttps(),
        }
