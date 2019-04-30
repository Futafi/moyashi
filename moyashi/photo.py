"""
画像から漫画のタイトルを取得するモジュールです。

: Examples
    >>> from photo import Photo
    >>> photo = Photo("YOUR-API-KEY", "PHOTO-URL")
    >>> photo.google_similar_photo()
    photo title
    >>> photo.vision_api()
    photo's text
    >>> photo.parse_text()
    parsed_text
    >>> photo.google_books_search()
    book titles

"""
from bs4 import BeautifulSoup
from .parser import BaseParser
import requests
import json


class Photo:
    def __init__(self, vision_api_key, photo_url="", parser=BaseParser):
        """
        Parameters
        ----------
        vision_api_key : str
            google vision api の api keyです。
        photo_url : str
            検索したい画像のURLです。ここで代入しなかった場合google_similar_photo()とvision_api()でURLを代入する必要があります。
        """
        self.photo_url = photo_url
        self.vision_api_key = vision_api_key
        self.vision_url = "https://vision.googleapis.com/v1/images:annotate?key=" + self.vision_api_key
        self.similar_photo_base_url = "https://images.google.com/searchbyimage?hl=ja-JP&image_url="
        self.google_books_base_url = "https://www.googleapis.com/books/v1/volumes?q=search+"
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0"}
        self.json_req = {
            "requests": [{"image": {"source": {"imageUri": ""}}, "features": [{"type": "TEXT_DETECTION", }]}]}
        self.text = ""
        self.parsed_text = ""
        self.parser = parser

    def google_similar_photo(self, photo_url=""):
        """
        google画像検索で予測される画像のタイトルを取得します。

        Parameters
        ----------
        photo_url : str
            検索したい画像のurlです。クラスを初期化する際にphoto_urlを代入した場合、検索が二回目以降の場合はオプションです。

        Returns
        -------
        title : str
            予測結果です。

        """
        if photo_url:
            self.photo_url = photo_url
        elif not self.photo_url:
            raise TypeError("検索する画像のURLを指定してください。")
        url = self.similar_photo_base_url + self.photo_url
        res = requests.get(url, headers=self.headers)
        res.raise_for_status()
        soup = BeautifulSoup(res.content, "html.parser")
        a = soup.select_one(".fKDtNb")
        title = a.string
        return title

    def vision_api(self, photo_url=""):
        """
        vision apiを使って画像からテキストを抽出します。

        Parameters
        ----------
        photo_url : str
            検索したい画像のurlです。クラスを初期化する際にphoto_urlを代入した場合、検索が二回目以降の場合はオプションです。

        Returns
        -------
        text : str
            vision apiで抽出したテキストです。

        """
        if photo_url:
            self.photo_url = photo_url
        elif not self.photo_url:
            raise TypeError("検索する画像のURLを指定してください。")
        self.json_req["requests"][0]["image"]["source"]["imageUri"] = self.photo_url
        res = requests.post(self.vision_url, json=self.json_req)
        res.raise_for_status()
        json_res = json.loads(res.text)
        self.text = json_res["responses"][0]["fullTextAnnotation"]["text"]
        return self.text

    def parse_text(self, text="", **kwargs):
        """
        vision apiで抽出したテキストをgoogle books api用にパースします。

        Parameters
        ----------
        text : str
            パースしたいテキストです。

        Returns
        -------
        parsed_text : str
            パースしたテキストです。
        """
        if text:
            self.text = text
        elif not self.text:
            raise TypeError("パースする文字列を指定してください。")
        if kwargs.get("parser"):
            self.parser = kwargs["parser"]
        self.parsed_text = self.parser(self.text).parse_text()
        return self.parsed_text

    def google_books_search(self, parsed_text="", is_only_comics=True):
        """
        google books search api を使ってテキストから本（たぶん漫画のみ）のタイトルを取得します。

        Parameters
        ----------
        parsed_text : str
            テキストです。先にparse_text()を使った場合はオプションです。
        is_only_comics : bool, default True
            comicsのみを抽出したいときに使います。

        Returns
        -------
        titles : list
            検索で見つかった本（たぶん漫画のみ）のタイトルのリストです。

        """
        if parsed_text:
            self.parsed_text = parsed_text
        elif not self.parsed_text:
            raise TypeError("検索文字列を指定してください。")
        url = self.google_books_base_url + self.parsed_text
        res = requests.get(url)
        res.raise_for_status()
        json_ = json.loads(res.text)
        books = [book["volumeInfo"] for book in json_["items"]]
        titles = list()
        for book in books:
            if is_only_comics:
                if "comic" in book.get("categories", "Non_genre")[0].lower():
                    titles.append(book["title"])
            else:
                titles.append(book["title"])
        return titles
