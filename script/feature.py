
class SITE:
    def __init__(self, site):
        self.url = site["url"]
        self.html = site["html"]
        self.features = {}

    def extract(self):
        if len(self.url) > 12:
            self.features["long_url"] = 1
        else:
            self.features["long_url"] = 0
