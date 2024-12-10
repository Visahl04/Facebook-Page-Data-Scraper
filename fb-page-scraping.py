import requests
from lxml import html
import re,csv
from bs4 import BeautifulSoup
import pandas as pd
data = []


def fb_scrape(url):
    print(url)
    payload = {}
    headers = {
      'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
      'accept-language': 'en-US,en;q=0.9',
      'cache-control': 'max-age=0',
      'cookie': 'datr=7hNOZxgnxDW90fECfmVXJce2; sb=7hNOZ5ORU4cXpX069XCPnmPk; dpr=1.25; wd=1536x275',
      'dpr': '1.25',
      'priority': 'u=0, i',
      'sec-ch-prefers-color-scheme': 'dark',
      'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
      'sec-ch-ua-full-version-list': '"Google Chrome";v="131.0.6778.86", "Chromium";v="131.0.6778.86", "Not_A Brand";v="24.0.0.0"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-model': '""',
      'sec-ch-ua-platform': '"Windows"',
      'sec-ch-ua-platform-version': '"15.0.0"',
      'sec-fetch-dest': 'document',
      'sec-fetch-mode': 'navigate',
      'sec-fetch-site': 'none',
      'sec-fetch-user': '?1',
      'upgrade-insecure-requests': '1',
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
      'viewport-width': '1536'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    with open('hh1.html', 'w', encoding='utf-8') as ff:
      ff.write(response.text)
      ff.close()
    html_content = response.text
    soup = BeautifulSoup(html_content, "html.parser")

    try:
      name = soup.find("meta", {"property": "og:title"})
      name = name.get("content", "")
    except:
      name = ''


    try:
      phone_match = re.search(r'\+1\s\d{3}-\d{3}-\d{4}', html_content)
      phone_number = phone_match.group(0) if phone_match else "Phone number not found"
    except:
      phone_number = ''

    try:
      address_match = html_content.split('"__isWebLinkable":"ExternalUrl","web_link":{"__typename":"ExternalWebLink","url":"https:\/\/maps.google.com')[1].split('"timeline_context_list_item_type":"INTRO_CARD_PROFILE_PHONE"}}}')[0]
      address = address_match.split('}},"associated_page_id":')[0].split(',"color_ranges":[],"text":')[1]
      address = address.split('"')[1]
    except:
      address = ''

    try:
      email_match = html_content.split('"__isWebLinkable":"ExternalUrl","web_link":{"__typename":"ExternalWebLink","url":"https:\/\/maps.google.com')[1].split('"timeline_context_list_item_type":"INTRO_CARD_PROFILE_EMAIL"}}},{"icon_image"')[0]
      email = email_match.split('_context_list_item_type":"INTRO_CARD_ADDRESS"}}},')[1].split('__module_operation_ProfileCometTileContextListViewItem_profileTileItem"')[1].split('aggregated_ranges":[],"ranges":[],"color_ranges":[]')[1].split(',"text":"')[1].split('"}},"')[0]
    except:
      email = ''

    temp = {
        "url":url,
        "Name": name,
        "Address": address,
        "Phone Number": phone_number,
        "email":email
    }
    data.append(temp)
    print(temp)


if __name__ == "__main__":
  with open('get-links.csv', 'r', encoding='utf-8') as ff:
    reader = csv.DictReader(ff)
    for row in reader:
        fb_scrape(row['url'])


  pt = pd.DataFrame(data)
  pt.to_csv('leads1.csv')