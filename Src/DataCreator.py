import BlockMaker
import pandas as pd


class DataCreator:
    def __init__(self):
        self.blockmaker = BlockMaker.BlockMaker()

    def getblocklist(self, url):
        self.blockmaker.seturl(url)
        return self.blockmaker.makeblock()

    def makecsv(self, urls, mode):
        cnt = 0
        newcsv = pd.DataFrame()
        for url in urls:
            self.__BlockList = self.getblocklist(url)
            for block in self.__BlockList:
                newblock = pd.DataFrame([[block.content, block.x, block.y, block.w, block.h, block.fontsize]])
                newcsv = pd.concat([newcsv, newblock])
            newcsv = pd.concat([newcsv, pd.DataFrame([[0, 0, 0, 0, 0]])])
            print(url, cnt)
            cnt += 1
        if mode == 1:
            newcsv.to_csv("./dataset/unlabeled_news.csv", index=False, header=False, encoding="utf-8")
        elif mode == 2:
            newcsv.to_csv("./dataset/unlabeled_blog.csv", index=False, header=False, encoding="utf-8")
        elif mode == 3:
            newcsv.to_csv("./dataset/unlabeled_shop.csv", index=False, header=False, encoding="utf-8")