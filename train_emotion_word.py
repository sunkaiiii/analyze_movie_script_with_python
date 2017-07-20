# -*- coding: utf-8 -*-
from matplotlib import pyplot
import scipy as sp
import numpy as np
from sklearn.datasets import load_files
from sklearn.cross_validation import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import classification_report
from sklearn.externals import joblib
import scipy as sp

pos_file=open('emotion/pos.txt')
neg_file=open('emotion/neg.txt')
pos=pos_file.read().split('\n')
neg=neg_file.read().split('\n')
pos_tag=np.ones(len(pos),dtype=int).tolist()
neg_tag=np.zeros(len(neg),dtype=int).tolist()
x_train=neg
x_train.extend(pos)
y_train=neg_tag
y_train.extend(pos_tag)
x_train, x_test, y_train, y_test \
    = train_test_split(x_train, y_train, test_size=0.1)
# # BOOL型特征下的向量空间模型，注意，测试样本调用的是transform接口
count_vec = TfidfVectorizer(binary=False, decode_error='ignore')
sp.save('train_data.npy',x_train)
x_train = count_vec.fit_transform(x_train)
clf = MultinomialNB().fit(x_train, y_train)
x_test=['垃圾 的 马桶 质量 感觉 非常糟糕','舒适 的 卫生 环境']
x_test = count_vec.transform(x_test)

y_test=[0,1]


# joblib.dump(clf,'emotion_model.model')
doc_class_predicted = clf.predict(x_test)
print(doc_class_predicted)
print(clf.predict_proba(x_test))