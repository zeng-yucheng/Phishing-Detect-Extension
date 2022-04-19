"""
This part is completed by Peng Yongxue
Analyze website features which will be used to predict whether it's a phishing website

1: Phishing
0: Legitimate
"""

import util
import re
import requests
import whois

from datetime import datetime
from urllib.parse import urlparse
from bs4 import BeautifulSoup

class SITE:
    def __init__(self, url, html):
        self.url = url
        self.html = html
        self.features = {}

    def analyze(self):
        self.analyze_url()
        self.analyze_html_content()

        return self.features
    
    def analyze_url(self):
        self.check_internet_protocol()
        self.check_url_length()
        self.check_short_url()
        self.contain_at_symbol()
        self.check_for_redirect()
        self.check_domain()
        self.check_domain_expiry_date()

    def analyze_html_content(self):
        page = requests.get(self.url)
        soup = BeautifulSoup(page.content, "html.parser")

        self.check_percentage_of_anchor_url(soup)
        self.check_form_handler(soup)
        return True

    # analyze url
    def check_internet_protocol(self):
        if self.url[0:5].upper() == "HTTPS":
            self.features[util.HTTPS_PROTOCOL] = 0
        else:
            self.features[util.HTTPS_PROTOCOL] = 1

    def check_url_length(self):
        if len(self.url) >= 54:
            self.features[util.LONG_URL] = 1
        else:
            self.features[util.LONG_URL] = 0

    def check_short_url(self):
        if re.search(util.SHORT_URL_PATTERN, self.url):
            self.features[util.SHORT_URL] = 1
        else:
            self.features[util.SHORT_URL] = 0

    def contain_at_symbol(self):
        if "@" in self.url:
            self.features[util.CONTAIN_AT_SYMBOL] = 1
        else:
            self.features[util.CONTAIN_AT_SYMBOL] = 0

    def check_for_redirect(self):
        position = self.url.rfind("//")
        if position > 6:
            self.features[util.CONTAIN_REDIRECT] = 1
        else:
            self.features[util.CONTAIN_REDIRECT] = 0

    def check_domain(self):
        domain = urlparse(self.url).netloc
        if "-" in domain:
            self.features[util.SEPARATED_BY_DASH_SYMBOL] = 1
        else:
            self.features[util.SEPARATED_BY_DASH_SYMBOL] = 0

        domain_upper = domain.upper()
        if "HTTPS" in domain_upper:
            self.features[util.EXISTENCE_OF_HTTPS] = 1
        else:
            self.features[util.EXISTENCE_OF_HTTPS] = 0

    def check_domain_expiry_date(self):
        domain = urlparse(self.url).netloc
        domainInfo = whois.query(domain)
        expiryDate = domainInfo.expiration_date

        today = datetime.today()
        
        if expiryDate:
            numOfDays = abs((expiryDate - today).days)

        if numOfDays <= 365:
            self.features[util.DOMAIN_EXPIRY_DATE] = 1
        else:
            self.features[util.DOMAIN_EXPIRY_DATE] = 0

    # analyze html content
    def check_percentage_of_anchor_url(self, soup):
        totalCounts = 0
        unsafeAnchorCounts = 0

        for anchor in soup.find_all('a', href=True):
            href = anchor['href'].lower()
            if "#" in href or "javascript" in href or "mailto" in href:
                unsafeAnchorCounts = unsafeAnchorCounts + 1
            totalCounts = totalCounts + 1

        percentage = 0
        if totalCounts != 0:
            percentage = unsafeAnchorCounts * 100 / float(totalCounts)
        
        if percentage < 31.0:
            self.features[util.PERCENTAGE_OF_URL_ANCHOR] = 0
        else:
            self.features[util.PERCENTAGE_OF_URL_ANCHOR] = 1

    def check_form_handler(self, soup):
        for form in soup.find_all('form', action=True):
            if len(form['action']) == 0 or form['action'] == "about:blank":
                self.features[util.BLANK_FORM_HANDLER] = 1
            else:
                self.features[util.BLANK_FORM_HANDLER] = 0