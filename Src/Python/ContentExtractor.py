from sklearn.externals import joblib
from sklearn.svm import SVC


class ContentExtractor:
    def __init__(self, mode):
        self.mode = mode
        if mode == 1: # 뉴스 카테고리
            self.classifier_path = "../../Model\svm_news.pkl" # 본문 분류 SVM 모델
            self.classifier_title_path = "../../Model\svm_news_title.pkl" # 제목 분류 SVM 모델
            self.sc_path = "../../Model\sc_news.pkl" # 본문 분류 StandardScaler 모델
            self.sc_title_path = "../../Model\sc_news_title.pkl" # 제목 분류 StandardScaler 모델
        elif mode == 2: # 블로그 카테고리
            self.classifier_path = "../../Model\svm_blog.pkl"
            self.classifier_title_path = "../../Model\svm_blog_title.pkl"
            self.sc_path = "../../Model\sc_blog.pkl"
            self.sc_title_path = "../../Model\sc_blog_title.pkl"
        elif mode == 3: # 쇼핑몰 카테고리
            self.classifier_path = "../../Model\svm_shop.pkl"
            self.classifier_title_path = "../../Model\svm_shop_title.pkl"
            self.sc_path = "../../Model\sc_shop.pkl"
            self.sc_title_path = "../../Model\sc_shop_title.pkl"

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
        self.boxes = []
        for block in self.BlockList: # BlockMaker에서 받은 블록 리스트를 순회
            x = [block.x, block.y, block.w, block.h, block.fontsize] # 블록의 5차원 feature를 input으로 저장
            self.inputs.append(x)
        self.pred = self.classifier.predict(self.sc.transform(self.inputs)) # SVM 모델에 블록을 입력해 본문인지 아닌지 분류

        for index in range(len(self.BlockList)): # 블록 리스트를 다시 한번 순회
            block = self.BlockList[index]
            if self.pred[index] == 1: # 모델이 본문으로 분류한 블록들을 제목 분류 SVM 모델에 입력
                x = [block.x, block.y, block.w, block.h, block.fontsize]
                self.boxes.append([block.x, block.y, block.w, block.h])
                self.title_inputs.append(x)
                self.contents.append([block.type, block.content])
        self.pred_title = self.classifier_title.predict(self.sc_title.transform(self.title_inputs)) # 제목 분류
        self.title = []
        self.image = []
        self.text = []
        for index in range(len(self.contents)): # 제목, 텍스트, 이미지 출력
            content = self.contents[index]
            if self.pred_title[index] == 1:
                self.title.append(content[1])
            elif content[0] == "text":
                self.text.append(content[1])
            elif content[0] == "img":
                self.image.append(content[1])
        return self.title, self.text, self.image, self.boxes
