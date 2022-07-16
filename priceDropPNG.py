import re
import imgkit
import os
import platform
import requests
from bs4 import BeautifulSoup
from requests.api import head

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'
}

htmlCode = """<html style="width:1982.09344px;height:1132.62482px"><head><link rel="preconnect" href="https://fonts.googleapis.com"> 
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin> 
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+Display:wght@700&display=swap" rel="stylesheet">
</head><body style="width:100%;height:100%;margin:0;"'>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 1982.09338 1132.62488">
  <defs>
    <clipPath id="a">
      <rect x="1210.00795" y="257.56638" width="670.08085" height="671.52767" rx="40.19084" style="fill:none" />
    </clipPath>
  </defs>
  <rect width="1982.09338" height="1132.62488" style="fill:#fb2" />
  <rect x="89.74013" y="257.56638" width="1039.18333" height="671.52762" style="fill:none" /><text text-anchor="start" transform="translate(257.05823 1069.40845)" style="text-align: center;isolation:isolate;font-size:129.02639770507812px;font-family:Noto Sans Display, sans-serif;font-weight:700">{} to {}</text><text transform="translate(609.33179 170.05463)" style="isolation:isolate;font-size:127.8889389038086px;font-family:Noto Sans Display, sans-serif;font-weight:700">PRICE DROP</text><path d="M1250.53113,257.56644h589.03454a40.45629,40.45629,0,0,1,40.52308,40.38922V888.571a40.45611,40.45611,0,0,1-40.38929,40.523h0q-.06683.00011-.13379,0H1250.53113a40.45634,40.45634,0,0,1-40.523-40.38934V298.572A40.87129,40.87129,0,0,1,1250.53113,257.56644Z" style="fill:#fff;stroke:#fff429;stroke-miterlimit:10;stroke-width:10px" />
  <g style="clip-path:url(#a)">
    <image width="604" height="605" transform="translate(1210.00795 257.56638) scale(1.10941 1.10996)" xlink:href="{}" />
  </g>
  <foreignObject x="89.74013" y="257.56638" width="1039.18333" height="671.52762">
    <div xmlns="http://www.w3.org/1999/xhtml" style="text-align: justify;font-size:65px;font-family:Noto Sans Display, sans-serif;font-weight:700">{}</div>
  </foreignObject>
</svg></body></html>"""

options = {
        'format': 'jpeg', 
        'quality': 100,
        'enable-local-file-access': "",
    }

def getPriceDropPNG(name, oldPrice, newPrice, imgLink):
    response = requests.get(imgLink, headers=headers)
    print(response)
    if (platform.system() == 'Darwin'):
        config = imgkit.config()
    else:
        config = imgkit.config(wkhtmltoimage='./bin/wkhtmltoimage')
    print("Generating JPEG for " + name + "...")
    html = htmlCode.format(oldPrice, newPrice, imgLink, name)
    outputPath = './tmp/'+name.split()[0]+'.jpeg'
    if os.path.exists(outputPath):
        os.remove(outputPath)
        print('Removed old file')
    try:
      imgkit.from_string(html, outputPath, options=options, config=config)
      return outputPath
    except Exception as e:
      print(e)
      return ""
