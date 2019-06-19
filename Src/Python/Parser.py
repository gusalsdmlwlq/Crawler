import Node
import subprocess


class Parser:
    def __init__(self):
        self.__url = ""
        self.__width = 0
        self.__height = 0
        self.geturl = ""

    def parsehtml(self): # url을 Node.js에 전달
        response = subprocess.Popen('node ../Node/Parser.js', stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True) # 파이프 연결
        result = response.communicate(input=self.__url.encode())[0]
        result = result.decode("utf-8").split('\n') # Node.js에서 노드 정보를 받음
        result = result[0:len(result)-1] # 노드 정보
        self.__width = result[len(result)-3] # 페이지 넓이
        self.__height = result[len(result)-2] # 페이지 높이
        self.geturl = result[len(result)-1] # 페이지 url
        node = []
        for i in range(0, len(result)-3): # 노드 정보를 특징값들로 나눔
            if i % 9 == 0:
                node.clear()
            node.append(result[i])
            if i % 9 == 8:
                self.makenode(node)


    def makenode(self, node): # 노드 정보를 노드 리스트에 저장
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