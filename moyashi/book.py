from .photo import Photo
import requests
import json


class Book:
    def __init__(self, vision_api_key="", title="", isbn13=None, isbn10=None,
                 url_rakuten="", url_amazon="", url_google=""):
        self.photo = Photo(vision_api_key)
        self.title = title
        self.title_gps = ""
        self.title_vision = ""

        self.title_amazon = ""
        self.isbn13 = isbn13
        self.isbn10 = isbn10
        self.url_rakuten = url_rakuten
        self.url_amazon = url_amazon
        self.url_google_books = url_google
        self.google_books_base_url = "https://www.googleapis.com/books/v1/volumes?q=intitle:"
        self.match_rate = 0

    def search_in_rakuten(self, title: str = ""):
        if title:
            self.title = title
        return self.url_rakuten

    def search_in_amazon(self, title: str = ""):
        if title:
            self.title = title
        return self.url_amazon

    def search_in_google_books(self, title: str = ""):
        if title:
            self.title = title
        return self.url_google_books
