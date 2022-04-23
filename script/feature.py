"""
This part is completed by Yongxue Peng
Analyze website features which will be used to predict whether it's a phishing website

1: Legitimate
-1: Phishing
"""

import util
import re
import requests
import whois

from urllib.parse import urlparse
from datetime import datetime
from bs4 import BeautifulSoup

class SITE:
    def __init__(self, url, html):
        self.url = url
        self.html = html
        self.features = {}

    def analyze(self):
        self.analyze_url()
        self.analyze_domain()
        self.analyze_html_content()

        return self.features
    
    def analyze_url(self):
        self.check_url_length()
        self.check_short_url()
        self.contain_at_symbol()
        self.check_for_redirect()

    def analyze_domain(self):
        domain = urlparse(self.url).netloc
        domainInfo = whois.query(domain)

        self.check_domain(domain)
        self.check_domain_expiry_date(domainInfo)
        self.check_hostname(domainInfo)
        self.check_domain_age(domainInfo)

    def analyze_html_content(self):
        page = requests.get(self.url)
        soup = BeautifulSoup(page.content, "html.parser")

        self.check_percentage_of_anchor_url(soup)
        self.check_form_handler(soup)

    # analyze url
    def check_url_length(self):
        if len(self.url) >= 54:
            self.features[util.LONG_URL] = -1
        else:
            self.features[util.LONG_URL] = 1

    def check_short_url(self):
        if re.search(util.SHORT_URL_PATTERN, self.url):
            self.features[util.SHORT_URL] = -1
        else:
            self.features[util.SHORT_URL] = 1

    def contain_at_symbol(self):
        if "@" in self.url:
            self.features[util.CONTAIN_AT_SYMBOL] = -1
        else:
            self.features[util.CONTAIN_AT_SYMBOL] = 1

    def check_for_redirect(self):
        position = self.url.rfind("//")
        if position > 6:
            self.features[util.CONTAIN_REDIRECT] = -1
        else:
            self.features[util.CONTAIN_REDIRECT] = 1

    # analyze domain
    def check_domain(self, domain):
        if "-" in domain:
            self.features[util.SEPARATED_BY_DASH_SYMBOL] = -1
        else:
            self.features[util.SEPARATED_BY_DASH_SYMBOL] = 1

    def check_hostname(self, domainInfo):
        hostname = domainInfo.name

        if re.search(hostname, self.url):
            self.features[util.URL_CONTAINS_HOSTNAME] = 1
        else:
            self.features[util.URL_CONTAINS_HOSTNAME] = -1

    def check_domain_expiry_date(self, domainInfo):
        expiryDate = domainInfo.expiration_date

        today = datetime.today()
        
        if expiryDate:
            numOfDays = abs((expiryDate - today).days)

        if numOfDays <= 365:
            self.features[util.DOMAIN_EXPIRY_DATE] = -1
        else:
            self.features[util.DOMAIN_EXPIRY_DATE] = 1

    def check_domain_age(self, domainInfo):
        createdAt = domainInfo.creation_date
        expiredAt = domainInfo.expiration_date

        if createdAt and expiredAt:
            domainAgeInDays = (expiredAt - createdAt).days
            domainAge = domainAgeInDays/30

            if domainAge < 6:
                self.features[util.DOMAIN_AGE] = -1
            else:
                self.features[util.DOMAIN_AGE] = 1

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
            self.features[util.PERCENTAGE_OF_URL_ANCHOR] = 1
        else:
            self.features[util.PERCENTAGE_OF_URL_ANCHOR] = -1

    def check_form_handler(self, soup):
        for form in soup.find_all('form', action=True):
            handler = form['action']
            if len(handler) == 0 or handler == "about:blank":
                self.features[util.BLANK_FORM_HANDLER] = -1
            else:
                self.features[util.BLANK_FORM_HANDLER] = 1

            if "mailto:" in handler or "mail()" in handler:
                self.features[util.SUBMIT_USER_INFO_TO_MAIL] = -1
            else:
                self.features[util.SUBMIT_USER_INFO_TO_MAIL] = 1