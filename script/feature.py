"""
This part belong to Peng Yongxue
Analyze website features which will be used to predict whether it's a phishing website
"""

import util
import re

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

    # Todo
    def analyze_html_content(self):
        return True

    def check_internet_protocol(self):
        if self.url[0:5].upper() == "HTTPS":
            self.features[util.HTTPS_PROTOCOL] = 1
        else:
            self.features[util.HTTPS_PROTOCOL] = 0

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