import requests
from flask import flash
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
import validators

class Scanner():
    
    ''' 
        Given a URL, it grabs all the HTML forms and then prints the number of forms detected.
        It then iterates all over the forms and submits them by putting the value of all text and search input fields with a Javascript code.
        If the Javascript code is injected and successfully executed, then the site has SXX vulnerability
        '''


    def __init__(self, url):
        self.url = url

    def validateUrl(self):
        ''' validate the url formaat and safety'''
        if not self.url:
            return False
        
        if not self.url.startswith(('http://', 'https://')):
            flash('Url must start with either "https://" or "http://" ')
            return False
        
        if not validators.url(self.url):
            flash('invalid url format!')
            return False
        
        return True

    def getAllForms(self):
        #Creates a get request with the stored url in the instance variable, and creates a soup obj
        soup = bs(requests.get(self.url).content, 'html.parser')
        #returns all form elements in the html as list
        return soup.find_all('form')
    
    def getFormDetails(self, form):
        details = {}
        #get from action attribute (target url)
        action = form.attrs.get('action','').lower()
        #get from method(post, get)
        method= form.attrs.get('method','get').lower()
      
        inputs = []

        #loop for ginding all input tags in the form
        for input_tag in form.find_all('input'):
            #gets the type, and defaults with text, then gets the name attribute
            input_type = input_tag.attrs.get('type', 'text')
            input_name = input_tag.attrs.get('name')
            inputs.append({'type':input_type, 'name': input_name})
        #stores all the collected information in the details dictionary with keys
        details["action"] = action
        details["method"] = method
        details["inputs"] = inputs
        return details
    
    def submitForm(self, form_details, value):
        """
        submits a form given in `form_details`
            form_details (list): a dictionary that contain form information
            url: the original URL that contain that form
            value : this will be replaced to all text and search inputs
        Returns the HTTP Response after form submission
        """
        target_url = urljoin(self.url, form_details['action'])
        inputs = form_details['inputs']
        data = {}
        
        for input in inputs:
            if input['type'] == 'text' or input['type'] == 'search':
                input['value'] = value
            input_name = input.get('name')
            input_value = input.get('value')
                # if input name and value are not None, 
                # then add them to the data of form submission
            if input_name and input_value:
                data[input_name] = input_value

        flash(f"Payload testing to {target_url}\n Data{data}")

        if form_details['method'] == 'post':
            return requests.post(target_url, data=data)
        else:
            return requests.get(target_url, params=data)

    def scanXss(self):
        '''SHows out any vulnerable forms if true, otherwise false'''
        forms = self.getAllForms()
        results = { 'url': self.url, 'form_count': len(forms), 'vulnerable_forms': []}

        # variable containing list of additional payloads, if the basic one gets easily filtered
        XSS_PAYLOADS = [
        "<script>alert('XSS')</script>",
        "<img src=x onerror=alert('XSS')>",
        "<svg/onload=alert('XSS')>",
        "'\"><script>alert('XSS')</script>",
        "<script>alert('Hope your site is secure =]')</script>"
        ]
        #Probably change this line to show something else...
        is_vulnerable = False

        for form in forms:
            form_detail = self.getFormDetails(form)
            for payload in XSS_PAYLOADS:
                try:
                    response = self.submitForm(form_detail, payload)
                    content = response.content.decode()
                    if payload in content:
                        results['vulnerable_forms'].append({
                            'details': form_detail,
                            'action': urljoin(self.url, form_detail['action'])
                        })
                        break

                except Exception as e:
                    flash(f'Testing form error:{payload} | {str(e)}')
                    continue
        return results
        

    # def SqlInjectionScan(self):


                    


