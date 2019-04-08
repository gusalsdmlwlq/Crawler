from sklearn.svm import SVC
import pandas as pd
import time
from sklearn.externals import joblib
from sklearn.model_selection import cross_val_score
import numpy as np
from sklearn.exceptions import ConvergenceWarning
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
import warnings
warnings.filterwarnings('ignore', category=ConvergenceWarning, module='sklearn')


class LearningManager:
    def __init__(self, mode):
        self.mode = mode
        if mode == 1:  # news_content
            self.classifer_path = "model\svm_news.pkl"
            self.sc_path = "model\sc_news.pkl"
        elif mode == 2:  # news_title
            self.classifer_path = "model\svm_news_title.pkl"
            self.sc_path = "model\sc_news_title.pkl"
        elif mode == 3:  # blog_content
            self.classifer_path = "model\svm_blog.pkl"
            self.sc_path = "model\sc_blog.pkl"
        elif mode == 4:  # blog_title
            self.classifer_path = "model\svm_blog_title.pkl"
            self.sc_path = "model\sc_blog_title.pkl"
        elif mode == 5:  # shopping mall_content
            self.classifer_path = "model\svm_shop.pkl"
            self.sc_path = "model\sc_shop.pkl"
        elif mode == 6:  # shopping mall_title
            self.classifer_path = "model\svm_shop_title.pkl"
            self.sc_path = "model\sc_shop_title.pkl"

        try:
            self.classifer = joblib.load(self.classifer_path)
            self.sc = joblib.load(self.sc_path)
        except:
            self.classifer = SVC(random_state=1)
            self.sc = StandardScaler()
        self.x_train = []
        self.y_train = []
        self.x_test = []
        self.y_test = []

    def readdata(self, filedir):
        csv = pd.read_csv(filedir, header=None, encoding="utf-8")
        for index, row in csv.iterrows():
            if not (row[1] == 0.0 and row[2] == 0.0 and row[3] == 0.0 and row[4] == 0.0):
                block = [row[1], row[2], row[3], row[4], row[5]]
                self.x_train.append(block)
                self.y_train.append(row[6])

    def fit(self):
        self.classifer.fit(self.x_train_std, self.y_train)
        joblib.dump(self.classifer, self.classifer_path)

    def preprocessing(self):
        self.sc.fit(self.x_train)
        self.x_train_std = self.sc.transform(self.x_train)
        joblib.dump(self.sc, self.sc_path)

    def resetmodel(self):
        self.classifer = SVC(random_state=1)
        self.sc = StandardScaler()

    def setmodel(self, params):
        self.classifer = SVC(random_state=1, C=params["C"], gamma=params["gamma"], kernel=params["kernel"],
                             max_iter=params["max_iter"], class_weight=params["class_weight"])

    def eval_train(self):
        scores = cross_val_score(estimator=self.classifer, X=self.x_train_std, y=self.y_train, cv=5, n_jobs=-1,
                                 scoring="accuracy")
        print('Test CV accuracy scores: %s' % scores)
        print('Test CV accuracy: {0:.3f} +/- {1:.3f}'.format(np.mean(scores), np.std(scores)))
        scores = cross_val_score(estimator=self.classifer, X=self.x_train_std, y=self.y_train, cv=5, n_jobs=-1,
                                 scoring="f1_weighted")
        print('Test CV accuracy scores: %s' % scores)
        print('Test CV accuracy: {0:.3f} +/- {1:.3f}'.format(np.mean(scores), np.std(scores)))

    def readtest(self, filedir):  # [content, x, y, w, h, font_size, label]
        csv = pd.read_csv(filedir, header=None, encoding="utf-8")
        for index, row in csv.iterrows():
            if not (row[1] == 0.0 and row[2] == 0.0 and row[3] == 0.0 and row[4] == 0.0):
                block = [row[1], row[2], row[3], row[4], row[5]]
                self.x_test.append(block)
                self.y_test.append(row[6])
        self.x_test = self.sc.transform(self.x_test)

    def eval_test(self):
        y_pred = self.classifer.predict(self.x_test)
        print("Test accuracy : ", accuracy_score(y_pred, self.y_test))
        y_pred = self.classifer.predict(self.x_test)
        print("Test accuracy : ", f1_score(y_pred, self.y_test))

# news training
start = time.time()
learningmanager = LearningManager(1)
learningmanager.resetmodel()
learningmanager.readdata("dataset/train_news.csv")
learningmanager.preprocessing()
params = {"C": 10.0, "gamma": 0.2, "kernel": "rbf", "max_iter": 1500, "class_weight": {0: 0.1, 1: 0.9}}
learningmanager.setmodel(params)
learningmanager.fit()
learningmanager = LearningManager(2)
learningmanager.resetmodel()
learningmanager.readdata("dataset/train_news_title.csv")
learningmanager.preprocessing()
params = {"C": 0.1, "gamma": 0.2, "kernel": "rbf", "max_iter": 500, "class_weight": {0: 0.1, 1: 0.9}}
learningmanager.setmodel(params)
learningmanager.fit()
end = time.time()
print(end-start, "seconds")

# blog training
start = time.time()
learningmanager = LearningManager(3)
learningmanager.resetmodel()
learningmanager.readdata("dataset/train_blog.csv")
learningmanager.preprocessing()
params = {"C": 0.1, "gamma": 1.0, "kernel": "rbf", "max_iter": 500, "class_weight": None}
learningmanager.setmodel(params)
learningmanager.fit()
learningmanager = LearningManager(4)
learningmanager.resetmodel()
learningmanager.readdata("dataset/train_blog_title.csv")
learningmanager.preprocessing()
params = {"C": 100.0, "gamma": 1.0, "kernel": "rbf", "max_iter": 500, "class_weight": {0: 0.1, 1: 0.9}}
learningmanager.setmodel(params)
learningmanager.fit()
end = time.time()
print(end-start, "seconds")

# shop training
start = time.time()
learningmanager = LearningManager(5)
learningmanager.resetmodel()
learningmanager.readdata("dataset/train_shop.csv")
learningmanager.preprocessing()
params = {"C": 1.0, "gamma": 1.0, "kernel": "rbf", "max_iter": 1000, "class_weight": None}
learningmanager.setmodel(params)
learningmanager.fit()
learningmanager = LearningManager(6)
learningmanager.resetmodel()
learningmanager.readdata("dataset/train_shop_title.csv")
learningmanager.preprocessing()
params = {"C": 100.0, "gamma": 0.2, "kernel": "rbf", "max_iter": 500, "class_weight": {0: 0.2, 1: 0.8}}
learningmanager.setmodel(params)
learningmanager.fit()
end = time.time()
print(end-start, "seconds")