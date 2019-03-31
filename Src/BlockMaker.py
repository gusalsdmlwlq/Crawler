import Parser
import Block
import Node
import ContentExtractor


class BlockMaker:
    def __init__(self):
        self.parser = Parser.Parser()
        self.__url = ""
        self.x_th = 100
        self.y_th = 20
        self.font_th = 5
        self.__nodeset = []

    def makeblock(self):
        self.parser.parsehtml()
        self.w = self.parser.getwidth()
        self.h = self.parser.getheight()
        self.__NodeList = self.parser.getnodelist()
        #self.widthlist = []
        self.width = [0, self.w]
        for node in self.__NodeList:
            if len(self.__nodeset) == 0:   # 노드 리스트가 비어 있는 경우
                if node.type == "img":  # 처음 노드가 img
                    self.bindnodes(node)
                else:   # 처음 노드가 text
                    self.__nodeset.append(node)
                    self.width = [node.x-node.w/2, node.x+node.w/2]
            else:   # 노드 리스트가 이미 차 있는 경우
                if node.type == "img":  # 새로운 노드가 img
                    self.bindnodes(self.__nodeset)
                    self.bindnodes(node)
                else:   # 새로운 노드가 text
                    lastnode = self.__nodeset[len(self.__nodeset) - 1]
                    if lastnode.bg_color != node.bg_color or abs(lastnode.fontsize - node.fontsize) > self.font_th:  #bg_color나 fontsize가 다른 경우
                        self.bindnodes(self.__nodeset)
                        self.__nodeset.append(node)
                        self.width = [node.x-node.w/2, node.x+node.w/2]
                    else:   # 좌표로 체크
                        #   y좌표가 비슷한 노드를 묶음
                        if abs(lastnode.y - node.y) < 5 or abs((lastnode.y-lastnode.h/2) - (node.y-node.h/2)) < 5 or abs((lastnode.y+lastnode.h/2) - (node.y+node.h/2)) < 5:
                            if min(abs((node.x - node.w/2) - (lastnode.x + lastnode.w/2)),
                                   abs((node.x + node.w/2) - (lastnode.x - lastnode.w/2)),
                                   abs(node.x - lastnode.x)) < self.x_th:
                                left = min(self.width[0], node.x-node.w/2)
                                right = max(self.width[1], node.x+node.w/2)
                                self.width = [left, right]
                            else:
                                self.bindnodes(self.__nodeset)
                                self.width = [node.x - node.w / 2, node.x + node.w / 2]
                            self.__nodeset.append(node)
                        else:   # y좌표가 차이나는 노드들
                            if min(abs((node.y - node.h/2) - (lastnode.y + lastnode.h/2)),
                                   abs((node.y + node.h/2) - (lastnode.y - lastnode.h/2)),
                                   abs(node.y - lastnode.y)) >= self.y_th:
                                self.bindnodes(self.__nodeset)
                                self.width = [node.x - node.w / 2, node.x + node.w / 2]
                            else:
                                left = min(self.width[0], node.x - node.w / 2)
                                right = max(self.width[1], node.x + node.w / 2)
                                self.width = [left, right]
                            self.__nodeset.append(node)
        if len(self.__nodeset) > 0:
            self.bindnodes(self.__nodeset)
            self.__nodeset.clear()
        #print(len(self.__BlockList))
        return self.__BlockList

    def bindnodes(self, nodelist):
        if type(nodelist) == Node.Node:  # 노드가 하나
            node = nodelist
            block = Block.Block(node.type, node.content, node.x / self.w, node.y / self.h, node.w / self.w, node.h / self.h, node.fontsize)
        elif len(nodelist) == 1:
            node = nodelist[0]
            block = Block.Block(node.type, node.content, node.x / self.w, node.y / self.h, node.w / self.w, node.h / self.h, node.fontsize)
        else:   # 노드가 여러개
            x_sum = 0
            y_sum = 0
            content = ""
            fontsize = 0
            for node in nodelist:
                x_sum += node.x
                y_sum += node.y
                content = content + node.content + " "
                fontsize += node.fontsize
            #x_mean = x_sum / len(nodelist)
            #x = x_mean / self.w
            y_mean = y_sum / len(nodelist)
            y = y_mean / self.h
            fontsize = fontsize / len(nodelist)
            first = nodelist[0]
            last = nodelist[len(nodelist) - 1]
            if first.y == last.y:  # y좌표가 같은 노드들
                h = nodelist[0].h
                w = self.width[1] - self.width[0]
                left = self.width[0]
                #w = abs((last.x + last.w/2) - (first.x - first.w/2))
            else:   # 아닌 경우
                w = 0
                left = 0
                w = self.width[1] - self.width[0]
                left = self.width[0]
                h = abs((last.y + last.h/2) - (first.y - first.h/2))
            x = (left + w/2) / self.w
            w = w / self.w
            h = h / self.h
            block = Block.Block("text", content, x, y, w, h, fontsize)
        self.__BlockList.append(block)
        self.__nodeset.clear()
        #print(block.type, block.content, block.x, block.y, block.w, block.h, block.fontsize)
        self.width = [0, self.w]

    def seturl(self, url):
        self.__url = url
        self.__BlockList = []
        self.parser.seturl(self.__url)

    def getnodelist(self):
        return self.__NodeList

# blockmaker = BlockMaker()
# blockmaker.seturl("https://blog.naver.com/wlstngl/221456444824")
# blocklist = blockmaker.makeblock()
# extractor = ContentExtractor.ContentExtractor(2)
# extractor.setblocklist(blocklist)
# extractor.extractcontent()
