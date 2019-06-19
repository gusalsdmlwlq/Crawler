import BlockMaker
import ContentExtractor
import sys


class Crawler:
    def __init__(self, mode):
        self.blockmaker = BlockMaker.BlockMaker()
        self.url = ""
        self.mode = ""
        if mode == 1 or mode == "news":
            self.mode = " 1"
            self.extractor = ContentExtractor.ContentExtractor(1)
        elif mode == 2 or mode == "blog":
            self.mode = " 2"
            self.extractor = ContentExtractor.ContentExtractor(2)
        elif mode == 3 or mode == "shop":
            self.mode = " 3"
            self.extractor = ContentExtractor.ContentExtractor(3)
        else:
            raise ValueError("Select mode \"news\" or \"blog\" or \"shop\" for 1st argument!")
        self.titles = []
        self.texts = []
        self.images = []
        self.boxes = []

    def seturl(self, url):
        self.url = url

    def extract(self):
        self.blockmaker.seturl(self.url + self.mode) # BlockMaker에 url과 카테고리를 전달하고 블록 리스트를 받음
        blocklist = self.blockmaker.makeblock()
        self.extractor.setblocklist(blocklist) # 블록 리스트를 ContentExtractor에 전달해 블록을 분류
        self.titles, self.texts, self.images, self.boxes = self.extractor.extractcontent()

    def show(self):
        print("----<Title>----")
        for title in self.titles:
            print(title)
        print("----<Text>----")
        for text in self.texts:
            print(text)
        print("----<Image>----")
        for image in self.images:
            print(image)

crawler = Crawler("news")
crawler.seturl("https://news.naver.com/main/ranking/read.nhn?mid=etc&sid1=111&rankingType=popular_day&oid=119&aid=0002321301&date=20190405&type=1&rankingSeq=7&rankingSectionId=100 1")
crawler.extract()
crawler.show()

crawler = Crawler("blog")
crawler.seturl("https://blog.naver.com/rnldya12?Redirect=Log&logNo=221361755582")
crawler.extract()
crawler.show()

crawler = Crawler("shop")
crawler.seturl("http://shopping.interpark.com/product/productInfo.do?prdNo=5630810467&dispNo=008001087")
crawler.extract()
crawler.show()