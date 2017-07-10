from doujin_scrapper import Gallery, Image
from ScrapperException import ScrapperException
import requests
import bs4
import re
import random
import os
import time

class Nhentai:
    """Object that holds information and methods about the scrapped galleries and images used for the bot"""
    
    def __init__(self):
        self.pages = {}
        self.scrapper = Scrapper()
        self.count_pages = self.scrapper.scrap_page_count()

    def get_page(self, page):
        """ Returns a page, a list of Galleries and caches it if necesary """
        if(page < 1 or page > self.count_pages):
            raise ScrapperException("Error, ivalid page")

        galleries = []
        
        if(not self.pages.get(str(page))):  # If the page is not cached, scrap it
            print("page number {0} not cached, caching".format(page))
            galleries = self.scrapper.scrap_page(page)
            self.pages[str(page)] = galleries
        else:
            print("page number {0} cached".format(page))
            galleries = self.pages[str(page)]
        
        return galleries

    def get_random_gallery(self):   
        # Get list of galleries from random page
        gallery_page = random.randrange(self.count_pages)
        galleries = self.get_page(gallery_page)
        
        # Get a random gallery from the list of galleries
        gallery_index = random.randrange(len(galleries))
        picked_gallery = galleries[gallery_index]
        
        # Cache it if necesary
        if(not picked_gallery.cached):
            print("random gallery page {0} index {1} not cached".format(gallery_page, gallery_index))
            self.scrapper.scrap_gallery_images(picked_gallery)
        else:
            print("random gallery page {0} index {1} cached".format(gallery_page, gallery_index))
        
        return picked_gallery

    def get_gallery(self, page, index):
        """ Returns a Gallery object from a page and position and caches it if necesary"""
        galleries = self.get_page(page)

        if(index >= len(galleries) and index < 0):
            raise ScrapperException("Error, invalid index")

        gallery = galleries[index]

        if(not gallery.cached):
            print("gallery page {0} index {1} not cached".format(page, index))
            self.scrapper.scrap_gallery_images(gallery)
        else:
            print("gallery page {0} index {1} cached".format(page, index))

        return gallery

class Scrapper:
    """Object only intended for scrapping Nhentai pages"""

    url_character = "https://nhentai.net/character/kaede-takagaki"
    url_gallery = "https://nhentai.net/g/"
    url_base = "https://nhentai.net"
    url_image = "https://i.nhentai.net/galleries/"
    regex_int = re.compile('[\d]+')

    def __init__(self):
        pass

    def scrap_page_count(self):
        """ Gets the maximun number of pages """
        res = requests.get(Scrapper.url_character)
        parsed = bs4.BeautifulSoup(res.text, "html.parser")

        href_last = parsed.select("a.last")[0].attrs['href']
        last_page_str = Scrapper.regex_int.search(href_last).group()
        last_page = int(last_page_str)

        return last_page

    def scrap_page(self, page):
        """ Scraps a page and returns a list Gallery objects """
        params = {'page': page}
        res = requests.get(Scrapper.url_character, params=params)
        parsed = bs4.BeautifulSoup(res.text, "html.parser")

        # Select the main contents
        gallery_tags = parsed.select("a.cover")
        galleries = []
        for a_tag in gallery_tags:
            url = Scrapper.url_base + a_tag.attrs['href']
            gallery = self.scrap_gallery(url)   # Scrap the gallery
            galleries.append(gallery)

        return galleries

    def scrap_gallery(self, url):
        """ Scraps a gallery with no image links """
        res = requests.get(url)
        parsed = bs4.BeautifulSoup(res.text, "html.parser")

        # Get gallery id
        gallery_id = Scrapper.regex_int.search(url).group()

        # Get title name
        title = parsed.select_one("div#info h1").getText()
        #print("title: \n{0}\n".format(title))

        # Get gallery image count
        image_a_tags = parsed.select("a.gallerythumb")
        image_count = len(image_a_tags)
        #print("Images on this gallery: " + str(image_count))

        # Get gallery thumbail
        thumbail_tag = parsed.select_one("div#cover img")
        thumbail_url = thumbail_tag.attrs['data-src']

        gallery = Gallery(gallery_id, title, url, image_count, thumbail_url)

        return gallery

    def scrap_gallery_images(self, gallery):
        """ Scraps images from a Gallery object, sets the image cache of the Gallery object """
        res = requests.get(gallery.url)
        parsed = bs4.BeautifulSoup(res.text, "html.parser")

        image_a_tags = parsed.select("a.gallerythumb")
        images = []
        for a_tag in image_a_tags:
            href = a_tag.attrs['href']
            show_url = Scrapper.url_base + href
            image_url = self.scrap_show(show_url) # Scrap the image
            image = Image(image_url, gallery.id)
            time.sleep(0.10)
            images.append(image)
        
        # Set the image cache
        gallery.images = images
        gallery.cached = True
    
    def scrap_show(self, show_url):
        """ 
        Scraps image link from show_url, returns the url to the image
        """
        res = requests.get(show_url)
        parsed = bs4.BeautifulSoup(res.text, "html.parser")
        img_tag = parsed.select_one("img.fit-horizontal") # May not work well
        src = img_tag.attrs['src']
        
        return src