
class MODEL:
    def __init__(self):
        self.result = {}

    def predict(self, x):
        if x["long_url"] > 0.5:
            self.result["result"] = "Phishing"
            self.result["probability"] = 1.0
        else:
            self.result["result"] = "Safe"
            self.result["probability"] = 1.0
        return self.result
