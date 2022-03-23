import urllib.request
import sys

try:
    url = sys.argv[1]
except:
    print("Invalid url, using test url instead...")
    url = 'https://www.iis.net/?utm_medium=iis-deployment'
response = urllib.request.urlopen(url)
string = response.read()
codec = 'utf-8'
dir = 'D:/NUS/S2/CS5331/Proj/proj/data/html.txt'

try:
    print("Using UTF-8 to decode...")
    html = string.decode(codec, 'ignore')
    with open(dir, 'w') as f:
        f.write(html)
except:
    print("UTF-8 fails to write text, using GBK instead...")
    codec = 'gbk'
    html = string.decode(codec, 'ignore')
    with open(dir, 'w') as f:
        f.write(html)

print("Write successfully!\nfile: " + dir + "    Codec: " + codec)
