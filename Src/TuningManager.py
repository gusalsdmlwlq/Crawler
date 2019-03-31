import LearningManager
from matplotlib import pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
import numpy as np
from mlxtend.plotting import plot_decision_regions
from mpl_toolkits.mplot3d import Axes3D


class TuningManager:

    def __init__(self, mode):
        self.learningmanager = LearningManager.LearningManager(mode)
        self.learningmanager.resetmodel()

    def tuning(self, mode, params):
        if mode == 1:
            self.train_path = "dataset/train_news.csv"
            self.test_path = "dataset/test_news.csv"
        elif mode == 2:
            self.train_path = "dataset/train_news_title.csv"
            self.test_path = "dataset/test_news_title.csv"
        elif mode == 3:
            self.train_path = "dataset/train_blog.csv"
            self.test_path = "dataset/test_blog.csv"
        elif mode == 4:
            self.train_path = "dataset/train_blog_title.csv"
            self.test_path = "dataset/test_blog_title.csv"
        elif mode == 5:
            self.train_path = "dataset/train_shop.csv"
            self.test_path = "dataset/test_shop.csv"
        elif mode == 6:
            self.train_path = "dataset/train_shop_title.csv"
            self.test_path = "dataset/test_shop_title.csv"
        learningmanager = self.learningmanager
        learningmanager.resetmodel()
        learningmanager.readdata(self.train_path)
        learningmanager.preprocessing()

        if params["kernel"] == "poly":
            self.svm = SVC(random_state=1, C=params["C"], gamma=params["gamma"], kernel=params["kernel"],
                      degree=params["degree"], max_iter=params["max_iter"], class_weight=params["class_weight"])
        elif params["kernel"] == "rbf":
            self.svm = SVC(random_state=1, C=params["C"], gamma=params["gamma"], kernel=params["kernel"],
                      max_iter=params["max_iter"], class_weight=params["class_weight"])

        pca = PCA(n_components=2)
        sc = StandardScaler()
        x = learningmanager.x_train
        x = pca.fit_transform(x)
        x = sc.fit_transform(x)
        y = learningmanager.y_train
        self.svm.fit(x, y)
        y = np.array(y)
        y = y.astype(np.integer)

        plot_decision_regions(X=x, y=y, clf=self.svm, legend=2)
        plt.legend(loc='upper left')

        if params["kernel"] == "poly":
            plt.title(
                "C:{} / gamma:{} / kernel:{} / degree:{} / iter:{} / weight:{}".format(params["C"], params["gamma"],
                                                                                       params["kernel"],
                                                                                       params["degree"],
                                                                                       params["max_iter"],
                                                                                       params["class_weight"]))
        elif params["kernel"] == "rbf":
            plt.title("C:{} / gamma:{} / kernel:{} / iter:{} / weight:{}".format(params["C"], params["gamma"],
                                                                                 params["kernel"], params["max_iter"],
                                                                                 params["class_weight"]))
        plt.show()

        learningmanager.setmodel(params=params)
        learningmanager.eval_train()
        learningmanager.fit()
        learningmanager.readtest(self.test_path)
        learningmanager.eval_test()

    def plot(self, mode, flag):
        learningmanager = self.learningmanager
        learningmanager.resetmodel()
        if flag == "train":
            if mode == 1:
                self.path = "dataset/train_news.csv"
            elif mode == 2:
                self.path = "dataset/train_news_title.csv"
            elif mode == 3:
                self.path = "dataset/train_blog.csv"
            elif mode == 4:
                self.path = "dataset/train_blog_title.csv"
            elif mode == 5:
                self.path = "dataset/train_shop.csv"
            elif mode == 6:
                self.path = "dataset/train_shop_title.csv"
        elif flag == "test":
            if mode == 1:
                self.path = "dataset/test_news.csv"
            elif mode == 2:
                self.path = "dataset/test_news_title.csv"
            elif mode == 3:
                self.path = "dataset/test_blog.csv"
            elif mode == 4:
                self.path = "dataset/test_blog_title.csv"
            elif mode == 5:
                self.path = "dataset/test_shop.csv"
            elif mode == 6:
                self.path = "dataset/test_shop_title.csv"
        learningmanager.readdata(self.path)
        learningmanager.preprocessing()

        # x, y, w, h, font size 분포
        for i in range(0, 5):
            plt.hist(learningmanager.x_train_std[:, i], bins=100)
            plt.show()

        # x, y 분포
        y = learningmanager.y_train
        x_1 = []
        x_0 = []
        for i in range(len(y)):
            if y[i] == 1:
                x_1.append(learningmanager.x_train_std[i])
            else:
                x_0.append(learningmanager.x_train_std[i])
        x_1 = np.array(x_1)
        x_0 = np.array(x_0)
        plt.scatter(x=x_1[:, 0], y=x_1[:, 1], s=0.5, c="red")
        plt.scatter(x=x_0[:, 0], y=x_0[:, 1], s=0.5)
        plt.title("X,Y")
        plt.show()

        # x, y, w 분포
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(111, projection='3d')
        #     ax.view_init(0,60)
        ax.scatter(x_1[:, 0], x_1[:, 1], x_1[:, 2], s=0.5, c="red")
        ax.scatter(x_0[:, 0], x_0[:, 1], x_0[:, 2], s=0.5)
        plt.title("X,Y,W")
        plt.show()

        # PCA 확인
        pca = PCA()
        pca.fit(learningmanager.x_train_std)
        plt.bar(range(1, 6), pca.explained_variance_ratio_, alpha=0.5, align='center')
        plt.step(range(1, 6), np.cumsum(pca.explained_variance_ratio_), where='mid')
        plt.ylabel('Explained variance ratio')
        plt.xlabel('Principal components')
        plt.show()

        # PCA(3) 분포
        x = learningmanager.x_train
        pca = PCA(3)
        sc = StandardScaler()
        x = pca.fit_transform(x)
        x = sc.fit_transform(x)
        y = learningmanager.y_train
        x_1 = []
        x_0 = []
        for i in range(len(y)):
            if y[i] == 1:
                x_1.append(x[i])
            else:
                x_0.append(x[i])
        x_1 = np.array(x_1)
        x_0 = np.array(x_0)
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(111, projection='3d')
        #     ax.view_init(45,0)
        ax.scatter(x_1[:, 0], x_1[:, 1], x_1[:, 2], s=0.5, c="red")
        ax.scatter(x_0[:, 0], x_0[:, 1], x_0[:, 2], s=0.5)
        plt.title("PCA_3")
        plt.show()


tuning = TuningManager(1)
tuning.tuning(1, {"C": 10, "gamma": 0.2, "kernel": "rbf", "max_iter": 1500, "class_weight": {0: 0.1, 1: 0.9}})
tuning.plot(1, "train")
