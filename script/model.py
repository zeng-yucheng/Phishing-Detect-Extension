"""
This part is completed by Zeng Yucheng
Model call of main script
"""


import pickle
import numpy as np
from keras.models import load_model


def fnn(features):
    im = getImportance(features)
    test_model = load_model('../models/fnn.m5')
    features = np.array([list(features.values())])
    X = features.reshape((-1, 11))
    res = test_model.predict(X)
    result = 'Phishing' if res[0][0] > res[0][1] else 'Safe'
    probability = max(res[0][0], res[0][1]) / (res[0][0] + res[0][1])
    j = {'result': result, 'probability': probability}
    j['first'] = im[0]
    j['second'] = im[1]
    return j


def xgb(features):
    im = getImportance(features)
    test_xgb = pickle.load(open('D:/NUS/S2/CS5331/Proj/proj/Phishing-Detect-Extension/models/xgb.pickle.dat', 'rb'))
    features = np.array([list(features.values())])
    X = features.reshape((-1, 11))
    res = test_xgb.predict_proba(X)
    result = 'Phishing' if res[0][0] > res[0][1] else 'Safe'
    probability = max(res[0][0], res[0][1])
    j = {'result': result, 'probability': probability}
    j['first'] = im[0]
    j['second'] = im[1]
    return j


def getImportance(features):
    order = ['percentage_of_anchor_url', 'blank_form_handler', 'separated_by_dash_symbol', 'domain_age',
             'short_url', 'domain_expiry_date', 'long_url', 'contain_at_symbol', 'contain_redirect',
             'url_contains_hostname', 'submit_user_info_to_mail']
    im = []
    print(features)
    for k in order:
        if features[k] == -1 and len(im) <= 2:
            im.append(k)
    while len(im) < 2:
        im.append('None')
    return im



