import BlockMaker
import pandas as pd


class DataCreator:
    def __init__(self):
        self.blockmaker = BlockMaker.BlockMaker()

    def getblocklist(self, url): # BlockMaker에 url을 전달하고 블록 리스트를 받음
        self.blockmaker.seturl(url)
        return self.blockmaker.makeblock()

    def makecsv(self, urls, mode): # 블록 리스트를 순회하며 블록의 정보들을 CSV 파일로 생성
        cnt = 0
        newcsv = pd.DataFrame()
        for url in urls:
            self.blockmaker = BlockMaker.BlockMaker()
            self.__BlockList = self.getblocklist(url)
            for block in self.__BlockList:
                newblock = pd.DataFrame([[block.content, block.x, block.y, block.w, block.h, block.fontsize]])
                newcsv = pd.concat([newcsv, newblock])
            newcsv = pd.concat([newcsv, pd.DataFrame([[0, 0, 0, 0, 0]])]) # 직접 label을 부여해야하기 때문에 페이지를 구분하기 위한 표시
            print(url, cnt)
            cnt += 1
            time.sleep(3)
        if mode == 1: # 뉴스
            newcsv.to_csv("../../Dataset/unlabeled_news.csv", index=False, header=False, encoding="utf-8")
        elif mode == 2: # 블로그
            newcsv.to_csv("../../Dataset/unlabeled_blog.csv", index=False, header=False, encoding="utf-8")
        elif mode == 3: # 쇼핑몰
            newcsv.to_csv("../../Dataset/unlabeled_shop.csv", index=False, header=False, encoding="utf-8")

creator = DataCreator()

import time
start = time.time()
news = [
    "https://news.naver.com/main/hotissue/read.nhn?mid=hot&sid1=102&cid=1080997&iid=2987262&oid=005&aid=0001167116&ptype=052",
    "https://news.naver.com/main/read.nhn?mode=LSD&mid=shm&sid1=103&oid=025&aid=0002880476",
    "https://news.naver.com/main/read.nhn?mode=LSD&mid=shm&sid1=105&oid=011&aid=0003493068",
    "https://news.naver.com/main/read.nhn?mode=LSD&mid=shm&sid1=105&oid=016&aid=0001491422",
    "https://news.naver.com/main/read.nhn?mode=LSD&mid=shm&sid1=105&oid=018&aid=0004298590",
    "https://entertain.v.daum.net/v/20190124143606348?rcmd=re",
    "https://entertain.v.daum.net/v/20190124141332219?rcmd=re",
    "https://entertain.v.daum.net/v/20190124092917077",
    "https://entertain.v.daum.net/v/20190124124606430",
    "https://news.v.daum.net/v/20190124132453598",
    "https://news.nate.com/view/20190129n10213",
    "https://news.nate.com/view/20190129n03109",
    "https://news.nate.com/view/20190129n05985",
    "https://news.nate.com/view/20190129n02447",
    "https://news.sbs.co.kr/news/endPage.do?news_id=N1005117997&plink=STAND&cooper=NAVER",
    "https://news.sbs.co.kr/news/endPage.do?news_id=N1005118081&plink=STAND&cooper=NAVER",
    "http://sbsfune.sbs.co.kr/news/news_content.jsp?article_id=E10009357290&plink=STAND&cooper=NAVER",
    "http://sbsfune.sbs.co.kr/news/news_content.jsp?article_id=E10009373162",
    "http://sbsfune.sbs.co.kr/news/news_content.jsp?article_id=E10009373156",
    "http://sbsfune.sbs.co.kr/news/news_content.jsp?article_id=E10009372730",
    "http://news.jtbc.joins.com/html/502/NB11763502.html",
    "http://news.jtbc.joins.com/html/918/NB11761918.html?log=jtbc|news|outsider",
    "http://news.jtbc.joins.com/html/497/NB11763497.html?log=jtbc|news|outsider",
    "http://news.jtbc.joins.com/html/893/NB11762893.html",
    "http://news.kbs.co.kr/news/view.do?ncd=4126462",
    "http://news.kbs.co.kr/news/view.do?ncd=4126457",
    "https://news.naver.com/main/ranking/read.nhn?mid=etc&sid1=111&rankingType=popular_day&oid=081&aid=0002973793&date=20190130&type=1&rankingSeq=1&rankingSectionId=100",
    "https://news.naver.com/main/ranking/read.nhn?mid=etc&sid1=111&rankingType=popular_day&oid=025&aid=0002881768&date=20190130&type=1&rankingSeq=2&rankingSectionId=100",
    "https://news.naver.com/main/ranking/read.nhn?mid=etc&sid1=111&rankingType=popular_day&oid=020&aid=0003196115&date=20190130&type=1&rankingSeq=2&rankingSectionId=103",
    "https://news.naver.com/main/ranking/read.nhn?mid=etc&sid1=111&rankingType=popular_day&oid=277&aid=0004403906&date=20190130&type=1&rankingSeq=2&rankingSectionId=105",
    "https://news.naver.com/main/read.nhn?mode=LSD&mid=shm&sid1=101&oid=092&aid=0002158772",
    "https://news.naver.com/main/ranking/read.nhn?mid=etc&sid1=111&rankingType=popular_day&oid=008&aid=0004194689&date=20190327&type=1&rankingSeq=2&rankingSectionId=101",
    "https://news.naver.com/main/ranking/read.nhn?mid=etc&sid1=111&rankingType=popular_day&oid=016&aid=0001515209&date=20190327&type=1&rankingSeq=8&rankingSectionId=101",
    "https://news.naver.com/main/read.nhn?mode=LSD&mid=shm&sid1=101&oid=003&aid=0009136457",
    "https://news.naver.com/main/ranking/read.nhn?mid=etc&sid1=111&rankingType=popular_day&oid=366&aid=0000430117&date=20190327&type=1&rankingSeq=10&rankingSectionId=101",
    "https://news.naver.com/main/ranking/read.nhn?mid=etc&sid1=111&rankingType=popular_day&oid=025&aid=0002894618&date=20190327&type=1&rankingSeq=9&rankingSectionId=100",
    "https://news.naver.com/main/ranking/read.nhn?mid=etc&sid1=111&rankingType=popular_day&oid=001&aid=0010720854&date=20190327&type=1&rankingSeq=1&rankingSectionId=101",
    "https://news.naver.com/main/ranking/read.nhn?mid=etc&sid1=111&rankingType=popular_day&oid=079&aid=0003209050&date=20190327&type=1&rankingSeq=2&rankingSectionId=100",
    "https://news.naver.com/main/ranking/read.nhn?mid=etc&sid1=111&rankingType=popular_day&oid=020&aid=0003206953&date=20190327&type=1&rankingSeq=10&rankingSectionId=100",
    "https://news.naver.com/main/ranking/read.nhn?mid=etc&sid1=111&rankingType=popular_day&oid=025&aid=0002894570&date=20190327&type=1&rankingSeq=6&rankingSectionId=100",
    "https://news.naver.com/main/ranking/read.nhn?mid=etc&sid1=111&rankingType=popular_day&oid=025&aid=0002894619&date=20190327&type=1&rankingSeq=4&rankingSectionId=100",
    "https://news.naver.com/main/ranking/read.nhn?mid=etc&sid1=111&rankingType=popular_day&oid=005&aid=0001184815&date=20190327&type=1&rankingSeq=5&rankingSectionId=100",
    "https://news.naver.com/main/read.nhn?mode=LSD&mid=shm&sid1=100&oid=016&aid=0001515300",
    "https://news.naver.com/main/read.nhn?mode=LSD&mid=shm&sid1=102&oid=011&aid=0003527928",
    "https://news.naver.com/main/read.nhn?mode=LSD&mid=shm&sid1=104&oid=001&aid=0010720781",
    "https://news.sbs.co.kr/news/endPage.do?news_id=N1005193629&plink=TOP&cooper=SBSNEWSMAIN",
    "https://news.sbs.co.kr/news/endPage.do?news_id=N1005194234&oaid=N1005194247&plink=TOP&cooper=SBSNEWSEND",
    "https://news.sbs.co.kr/news/endPage.do?news_id=N1005192782&oaid=N1005194234&plink=POP&cooper=SBSNEWSEND",
    "https://news.sbs.co.kr/news/endPage.do?news_id=N1005192787&oaid=N1005192782&plink=POP&cooper=SBSNEWSEND",
    "https://news.sbs.co.kr/news/endPage.do?news_id=N1005194187",
    "https://news.sbs.co.kr/news/endPage.do?news_id=N1005192378",
    "https://news.sbs.co.kr/news/endPage.do?news_id=N1005192775&oaid=N1005192378&plink=TOP&cooper=SBSNEWSEND",
    "https://news.sbs.co.kr/news/endPage.do?news_id=N1005193157&oaid=N1005192775&plink=POP&cooper=SBSNEWSEND",
    "https://news.sbs.co.kr/news/endPage.do?news_id=N1005193625&oaid=N1005193157&plink=TOP&cooper=SBSNEWSEND",
    "http://news.jtbc.joins.com/html/904/NB11789904.html?log=jtbc|news|index_newsN_B",
    "http://news.jtbc.joins.com/html/538/NB11790538.html",
    "http://news.jtbc.joins.com/html/900/NB11789900.html",
    "http://news.jtbc.joins.com/html/497/NB11790497.html",
    "http://news.jtbc.joins.com/html/496/NB11790496.html",
    "http://news.jtbc.joins.com/html/504/NB11790504.html",
    "https://news.naver.com/main/read.nhn?oid=001&sid1=102&aid=0010721441&mid=shm&mode=LSD&nh=20190327110839",
    "https://news.naver.com/main/read.nhn?mode=LSD&mid=shm&sid1=103&oid=023&aid=0003435491",
    "https://news.naver.com/main/read.nhn?mode=LSD&mid=shm&sid1=102&oid=014&aid=0004200429",
    "https://news.naver.com/main/read.nhn?mode=LSD&mid=shm&sid1=101&oid=421&aid=0003903651",
    "https://news.naver.com/main/read.nhn?mode=LSD&mid=shm&sid1=105&oid=014&aid=0004199808",
    "https://news.naver.com/main/read.nhn?mode=LSD&mid=shm&sid1=103&oid=296&aid=0000040690",
    "https://news.naver.com/main/ranking/read.nhn?mid=etc&sid1=111&rankingType=popular_day&oid=011&aid=0003527978&date=20190327&type=1&rankingSeq=7&rankingSectionId=103",
    "https://news.naver.com/main/ranking/read.nhn?mid=etc&sid1=111&rankingType=popular_day&oid=310&aid=0000071782&date=20190327&type=1&rankingSeq=9&rankingSectionId=103",
    "https://news.naver.com/main/ranking/read.nhn?mid=etc&sid1=111&rankingType=popular_day&oid=092&aid=0002158752&date=20190327&type=1&rankingSeq=7&rankingSectionId=105",
    "https://news.naver.com/main/ranking/read.nhn?mid=etc&sid1=111&rankingType=popular_day&oid=022&aid=0003349846&date=20190327&type=1&rankingSeq=7&rankingSectionId=100"
]
blog = [
    "https://sset20.tistory.com/157",
    "https://tifa-lockhart.tistory.com/359",
    "https://prolite.tistory.com/1404",
    "https://itqnara.tistory.com/64"
]
shop = [
    "http://shopping.interpark.com/product/productInfo.do?prdNo=6431695606&dispNo=008022001",
    "http://shopping.interpark.com/product/productInfo.do?prdNo=6388995211&dispNo=008022001",
    "http://shopping.interpark.com/product/productInfo.do?prdNo=5409021275&dispNo=008022001",
    "http://shopping.interpark.com/product/productInfo.do?prdNo=204227717&dispNo=008001087",
    "http://shopping.interpark.com/product/productInfo.do?prdNo=6282942189&dispNo=008022001",
    "http://shopping.interpark.com/product/productInfo.do?prdNo=4115874046&dispNo=008001087",
    "http://item.gmarket.co.kr/detailview/item.asp?goodscode=1516490262",
    "http://item.gmarket.co.kr/Item?goodscode=1562572595",
    "http://shopping.interpark.com/product/productInfo.do?prdNo=4855016010",
    "http://shopping.interpark.com/product/productInfo.do?prdNo=5133915886&dispNo=008014004"
]

for i in range(len(news)):
    news[i] = news[i]+" 1"
for i in range(len(blog)):
    blog[i] = blog[i]+" 2"
for i in range(len(shop)):
    shop[i] = shop[i]+" 3"

creator.makecsv(news,1)
creator.makecsv(blog,2)
creator.makecsv(shop,3)
end = time.time()
print(end-start," secs")