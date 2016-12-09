from sklearn import tree
from sklearn.neural_network import MLPClassifier
from sklearn import svm
import numpy as np
import cv2

class Files:
    def __init__(self):
        self.content = []

    def getFile(self, filename):
        in_file = open(filename)
        self.content = [line.rstrip() for line in in_file]
        in_file.close()

    def printFile(self):
        for i in self.content:
            print(i)

    def returnList(self, filename):
        self.getFile(filename)
        return self.content

class Features:
    def __init__(self):
        self.features = []

    def readImages(self, file_name):
        img = cv2.imread(file_name)
        return img

    def createFeatureVector(self, start, end):
        images = []

        for k in range(start, end):
            img = self.readImages(str(k)+".png")
            row = 0
            col = 0
            color = 100
            box = []
            while (row < 576):
                for i in range(row, row+72):
                    if (i%72 != 0):
                        box.append([])
                        for j in range(col, col+60):
                            if (j%60 != 0):
                                box[(i%72)-1].append(img[i][j])
                col = col + 60
                images = np.reshape(box, len(box)*len(box[0])*3)
                self.features.append(images)
                box = []
                if (col >= 600):
                    row = row + 72
                    col = 0

    def returnFeatureVector(self, start, end):
        self.createFeatureVector(start, end)
        return self.features

features = Features()
feature = features.returnFeatureVector(1, 10)

label_file = Files()
label = label_file.returnList("label")

tests = Features()
test = tests.returnFeatureVector(20, 24)

svm_1 = svm.SVC(kernel = "linear")
svm_1 = svm_1.fit(feature, label)
classification = svm_1.predict(test)
out_file = open("out", "w")
zero = True
ctr = 0
classification = classification.tolist()

for i in classification:
    ctr = ctr+1
    if (i == '0' and zero == True):
        out_file.write(" ")
        zero = False
    elif (i != '0'):
        out_file.write(i)
        zero = True
    if (ctr == 80 and classification.index(i) != 0):
        ctr = 0
        out_file.write("\n")
