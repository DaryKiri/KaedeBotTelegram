from ScrapperException import ScrapperException
import os

class Gallery:
    def __init__(self, gallery_id=None, title="", url="", page_count=0, thumbail=""):
        self.id = gallery_id
        self.title = title
        self.url = url
        self.page_count = page_count
        self._image_cache = []
        self.cached = False
        self.thumbail = thumbail

    def clean(self):    #TODO
        pass

    # Properties (getter and setters)
    @property
    def images(self):
        if(not self.cached or not self._image_cache):
            raise ScrapperException("ERROR, cannot get list of inexistent images")
        else:
            return self._image_cache

    @images.setter
    def images(self, images):
        self._image_cache = images
        self.cached = True

class Image:    
    def __init__(self, url="", gallery_id=None, downloadable=False, on_disk=False):
        self.url = url
        self.gallery_id = gallery_id
        self.downloadable = downloadable
        self.on_disk = on_disk
        self._path = None

    def download(self): #TODO
        """ Downloads the image and sets the path with the relative path of the file downloaded """
        if(not self.downloadable):
            raise ScrapperException("ERROR, cannot download a not downloadable image")
        
        if(not self.on_disk): # TODO
            pass
        
        return self._path

    # Properties (getters and setters)
    @property
    def path(self):
        if(self._path is None):
            raise ScrapperException("ERROR, cannot get inexistent file path")
        else:
            return self._path