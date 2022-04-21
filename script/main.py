import urllib.request
import sys
from feature import SITE
from model import fnn, xgb

# Fetch url
try:
    url = sys.argv[1]
except:
    print("Invalid url, using test url instead...")
    url = 'https://www.iis.net/?utm_medium=iis-deployment'

if len(url) > 4:
    if url[:4] != "http":
        print("Please input valid http(s) url and try again.")

# Fetch html
response = urllib.request.urlopen(url)
string = response.read()
codec = 'utf-8'
dir = 'D:/NUS/S2/CS5331/Proj/proj/Phishing-Detect-Extension/data/dataset.txt'

try:
    print("Using UTF-8 to decode...")
    html = string.decode(codec, 'ignore')

except:
    print("UTF-8 fails to write text, using GBK instead...")
    codec = 'gbk'
    html = string.decode(codec, 'ignore')

print("Transfer Successfully!")

# For testing only
url = 'https://www.google.com'
fb = sys.argv[2]

if fb == '0':
    # Construct site class
    site = SITE(url, html)
    # features = site.analyze()
    features = [1 for i in range(11)]
    print(features)
    # Process features
    res = xgb(features)
    print(res)
else:
    with open(dir, "w") as f:
        f.write(url+' '+fb)
    print(url, fb)
