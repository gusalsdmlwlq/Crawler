import BlockMaker
import ContentExtractor
import sys


class Crawler:
    def __init__(self, mode):
        self.blockmaker = BlockMaker.BlockMaker()
        self.url = ""
        if mode == 1 or mode == "news":
            self.extractor = ContentExtractor.ContentExtractor(1)
        elif mode == 2 or mode == "blog":
            self.extractor = ContentExtractor.ContentExtractor(2)
        elif mode == 3 or mode == "shop":
            self.extractor = ContentExtractor.ContentExtractor(3)
        else:
            raise ValueError("Select mode \"news\" or \"blog\" or \"shop\" for 1st argument!")
        self.titles = []
        self.texts = []
        self.images = []

    def seturl(self, url):
        self.url = url

    def extract(self):
        self.blockmaker.seturl(self.url)
        blocklist = self.blockmaker.makeblock()
        self.extractor.setblocklist(blocklist)
        self.titles, self.texts, self.images = self.extractor.extractcontent()

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
crawler.seturl("https://news.naver.com/main/ranking/read.nhn?mid=etc&sid1=111&rankingType=popular_day&oid=119&aid=0002321301&date=20190405&type=1&rankingSeq=7&rankingSectionId=100")
crawler.extract()
crawler.show()

crawler = Crawler("blog")
crawler.seturl("https://blog.naver.com/eunji318/221505952095")
crawler.extract()
crawler.show()

crawler = Crawler("shop")
crawler.seturl("http://shopping.interpark.com/product/productInfo.do?prdNo=6087626322&dispNo=008022001")
crawler.extract()
crawler.show()