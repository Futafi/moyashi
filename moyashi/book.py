from .photo import Photo


class Book:
    def __init__(self, vision_api_key="", title="", isbn13=None, isbn10=None, url_rakuten="", url_amazon=""):
        self.vision_api_key = vision_api_key
        self.title = title
        self.title_gps = ""
        self.title_vision = ""

        self.title_amazon = ""
        self.isbn13 = isbn13
        self.isbn10 = isbn10
        self.url_rakuten = url_rakuten
        self.url_amazon = url_amazon
        self.match_rate = 0
