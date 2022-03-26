"""
This part belong to Peng Yongxue
Create features of SITE class using extract function
"""

import util

class SITE:
    def __init__(self, url, html):
        self.url = url
        self.html = html
        self.features = {}

    def extract(self):
        return self.features
        
    def check_url_length(self):
        if len(self.url) > 12:
            self.features[util.LONG_URL] = 1
        else:
            self.features[util.LONG_URL] = 0
