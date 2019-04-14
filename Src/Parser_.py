import Node
import subprocess
from confluent_kafka import Consumer, KafkaError, Producer

p = Producer({'bootstrap.servers': 'kafka:9092'})
c = Consumer({

    'bootstrap.servers': 'kafka:9092',

    'group.id': 'console-consumer-53678',

    'default.topic.config': {

        'auto.offset.reset': 'smallest'

    }

})


class Parser:
    def __init__(self):
        self.__url = ""
        self.__width = 0
        self.__height = 0
        self.geturl = ""

    def delivery_report(self, err, msg):
        if err is not None:
            print('Message delivery failed: {}'.format(err))
        else:
            print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

    def parsehtml(self):
        p.poll(0)
        p.produce('url', self.__url.encode('utf-8'), callback=self.delivery_report)
        p.flush()
        response = subprocess.Popen('node Parser_.js', stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        result = response.communicate(timeout=30)
        c.subscribe(['node'])
        msg = c.poll(1.0)
        print('Received message: {}'.format(msg.value().decode('utf-8')))
        c.close()
        result = msg.value().decode('utf-8').split('\n')
        result = result[0:len(result) - 1]
        self.__width = result[len(result) - 3]
        self.__height = result[len(result) - 2]
        self.geturl = result[len(result) - 1]
        node = []
        for i in range(0, len(result) - 3):
            if i % 9 == 0:
                node.clear()
            node.append(result[i])
            if i % 9 == 8:
                self.makenode(node)

    def makenode(self, node):
        newnode = Node.Node(node)
        if not (newnode.x >= self.getwidth() or newnode.y >= self.getheight()):
            self.__NodeList.append(newnode)
        # print(node)

    def getnodelist(self):
        return self.__NodeList

    def getwidth(self):
        return float(self.__width)

    def getheight(self):
        return float(self.__height)

    def seturl(self, url):
        self.__url = url
        self.__NodeList = []
