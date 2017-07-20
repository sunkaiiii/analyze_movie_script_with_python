from sklearn.externals import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
import scipy as sp
import jieba
clf=joblib.load('emotion_model.model')
count_vec = TfidfVectorizer(binary=False, decode_error='ignore')
x_train = sp.load('train_data.npy')
result=[]


def read_file_and_split_session(filename):
    return open(filename).read().split('\n\n')

def compare_emotion(x_test):
    count_vec.fit_transform(x_train)
    x_test = count_vec.transform(x_test)
    doc_class_predicted = clf.predict(x_test)
    # print(doc_class_predicted)
    print(clf.predict_proba(x_test))
    result.extend(doc_class_predicted)
    return doc_class_predicted

def read_session_lines(sessions):
    count=0
    for i in sessions:

sessions=read_file_and_split_session('bailuyuan.txt')
print(len(sessions))