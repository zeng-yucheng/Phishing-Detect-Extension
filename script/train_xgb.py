import numpy as np
from scipy.io import arff
import pandas as pd
from xgboost import XGBClassifier
import pickle
from sklearn.model_selection import train_test_split

data = arff.loadarff('../datasets/Training Dataset.arff')
df = pd.DataFrame(data[0]).astype('int')

# ---------need to use corresponding features------------- #
# df = df[[], [], ... ,[]]

X, y = df.values[:, :-1], df.values[:, -1]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=5331)

xgb = XGBClassifier(objective='binary:logistic', colsample_tree=0.3, learning_rate=0.1, max_depth=6,
                    alpha=10, n_estimators=10)
xgb.fit(X_train, y_train)
res = xgb.score(X_test, y_test)
print(res)

pickle.dump(xgb, open('../models/xgb.pickle.dat', 'wb'))
test_xgb = pickle.load(open('../models/xgb.pickle.dat', 'rb'))
# print(test_xgb.predict_proba(X_test))

# ---------further analyze the ROC curve, AUC value and feature importance----------- #

