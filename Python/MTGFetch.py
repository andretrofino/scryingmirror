import cv2
import urllib
import numpy as np
from bs4 import BeautifulSoup
import requests
import requests.packages.urllib3
import urlparse
import os


class MTGFetcher:

    def __init__(self):
        self.base_url = "http://gatherer.wizards.com/Pages/Search/Default.aspx?page=%s&sort=cn+&set="
        self.base_card_url = "http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=%s&type=card"
        self.expansions = [
            "[%20Eternal%22Masters%20]"
        ]

    def fetch_expansion(self, expansion, base_dir):

        # Image will be saved in a folder with the expansion name
        save_path = os.path.join(base_dir, expansion)

        if not os.path.exists(save_path):
            os.makedirs(save_path)

        print 'Retrieving ' + expansion

        page_url = self.base_url % str(0) + "[%22" + expansion + "%22]"
        data = requests.get(page_url).text
        soup = BeautifulSoup(data, "lxml-xml")

        card_titles = soup.find_all(class_='cardTitle')
        n_pages = len(soup.find_all(class_='pagingcontrols'))

        print 'Saving Images'
        print 'Number of pages ' + str(n_pages)

        # First result page
        for card in card_titles:
            card_name = card.a.contents[0]
            print card_name
            card_url = card.a['href'].encode('utf-8')
            card_id = card_url[card_url.find('=') + 1:]
            full_url = self.base_card_url % str(card_id)
            img = url_to_image(full_url)
            img_save_path = os.path.join(save_path, card_name + ".jpg")
            cv2.imwrite(img_save_path, img)

        # Other result pages
        for i in xrange(1, n_pages+1):
            page_url = self.base_url % str(i) + "[%22" + expansion + "%22]"
            data = requests.get(page_url).text
            soup = BeautifulSoup(data, "lxml-xml")
            card_titles = soup.find_all(class_='cardTitle')

            for card in card_titles:
                card_name = card.a.contents[0]
                print card_name
                card_url = card.a['href'].encode('utf-8')
                card_id = card_url[card_url.find('=') + 1:]
                full_url = self.base_card_url % str(card_id)
                img = url_to_image(full_url)
                img_save_path = os.path.join(save_path, card_name + ".jpg")
                cv2.imwrite(img_save_path, img)


def url_to_image(url):
    resp = urllib.urlopen(url)
    img = np.asarray(bytearray(resp.read()), dtype="uint8")
    img = cv2.imdecode(img, cv2.IMREAD_COLOR)

    return img


def main():
    fetcher = MTGFetcher()
    fetcher.fetch_expansion('Oath of the Gatewatch', 'Images')

if __name__ == "__main__":
    main()