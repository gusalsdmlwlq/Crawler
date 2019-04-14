import Node
import subprocess


class Parser:
    def __init__(self):
        self.__url = ""
        self.__width = 0
        self.__height = 0
        self.geturl = ""

    def parsehtml(self):
        response = subprocess.Popen('node Parser.js', stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        result = response.communicate(input=self.__url.encode())[0]
        result = result.decode("utf-8").split('\n')
        result = result[0:len(result)-1]
        self.__width = result[len(result)-3]
        self.__height = result[len(result)-2]
        self.geturl = result[len(result)-1]
        node = []
        for i in range(0, len(result)-3):
            if i % 9 == 0:
                node.clear()
            node.append(result[i])
            if i % 9 == 8:
                self.makenode(node)


    def makenode(self, node):
        newnode = Node.Node(node)
        if not(newnode.x >= self.getwidth() or newnode.y >= self.getheight()):
            self.__NodeList.append(newnode)
        #print(node)

    def getnodelist(self):
        return self.__NodeList

    def getwidth(self):
        return float(self.__width)

    def getheight(self):
        return float(self.__height)

    def seturl(self, url):
        self.__url = url
        self.__NodeList = []
'''
parser = Parser()
parser.seturl("https://news.naver.com/main/read.nhn?mode=LSD&mid=shm&sid1=103&oid=025&aid=0002880476")
parser.parsehtml()
'''