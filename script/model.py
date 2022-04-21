"""
This part belong to Xu Ye
Predict result in dictionary format using feature x
"""
import pickle
import numpy as np
from keras.models import load_model


def fnn(features):
    test_model = load_model('../models/fnn.m5')
    X = np.array(features).reshape(1, 11)
    res = test_model.predict(X)
    result = 'Phishing' if res[0][0] > res[0][1] else 'Safe'
    probability = max(res[0][0], res[0][1]) / (res[0][0] + res[0][1])
    return {'result': result, 'probability': probability}


def xgb(features):
    test_xgb = pickle.load(open('D:/NUS/S2/CS5331/Proj/proj/Phishing-Detect-Extension/models/xgb.pickle.dat', 'rb'))
    X = np.array(features).reshape(1, 11)
    res = test_xgb.predict_proba(X)
    result = 'Phishing' if res[0][0] > res[0][1] else 'Safe'
    probability = max(res[0][0], res[0][1])
    return {'result': result, 'probability': probability}
