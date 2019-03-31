from sklearn.externals import joblib
from sklearn.svm import SVC


class ContentExtractor:
    def __init__(self, mode):
        self.mode = mode
        if mode == 1:
            self.classifier_path = "model\svm_shop.pkl"
            self.classifier_title_path = "model\svm_shop_title.pkl"
            self.sc_path = "model\sc_shop.pkl"
            self.sc_title_path = "model\sc_shop_title.pkl"
        elif mode == 2:
            self.classifier_path = "model\svm_others.pkl"
            self.classifier_title_path = "model\svm_others_title.pkl"
            self.sc_path = "model\sc_others.pkl"
            self.sc_title_path = "model\sc_others_title.pkl"

        try:
            self.classifier = joblib.load(self.classifier_path)
            self.classifier_title = joblib.load(self.classifier_title_path)
            self.sc = joblib.load(self.sc_path)
            self.sc_title = joblib.load(self.sc_title_path)
        except:
            print("!!!\n\tNo learned model\n!!!")

    def setblocklist(self, blocklist):
        self.BlockList = blocklist

    def extractcontent(self):
        self.inputs = []
        self.title_inputs = []
        self.contents = []
        for block in self.BlockList:
            x = [block.x, block.y, block.w]
            self.inputs.append(x)
        self.pred = self.classifier.predict(self.sc.transform(self.inputs))
        for index in range(len(self.BlockList)):
            block = self.BlockList[index]
            if self.pred[index] == 1:
                x = [block.x, block.y, block.w, block.fontsize]
                self.title_inputs.append(x)
                self.contents.append([block.type, block.content])
        self.pred_title = self.classifier_title.predict(self.sc_title.transform(self.title_inputs))
        self.title = []
        self.image = []
        self.text = []
        for index in range(len(self.contents)):
            content = self.contents[index]
            if self.pred_title[index] == 1:
                self.title.append(content[1])
            elif content[0] == "text":
                self.text.append(content[1])
            elif content[0] == "img":
                self.image.append(content[1])
        print("\ttitle")
        for i in self.title:
            print(i)
        print("\ttext")
        for i in self.text:
            print(i)
        print("\timage")
        for i in self.image:
            print(i)
