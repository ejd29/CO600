import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import recall_score
from imblearn.over_sampling import SMOTE

dataset = pd.read_csv('Dataset.csv', ',')
dataset_attributes_X = dataset.columns.values[0:533].tolist()
dataset_attribute_Y = dataset.columns.values[533:534].tolist()

dataset_X = dataset[dataset_attributes_X].as_matrix()
#dataset_Y = pd.get_dummies(dataset[dataset_attribute_Y]).as_matrix()
dataset_Y = dataset[dataset_attribute_Y].as_matrix()

print(dataset_X.shape)
print(dataset_Y)

X_train, X_test, y_train, y_test = train_test_split(dataset_X, dataset_Y, test_size=0.2, random_state=12)

sm = SMOTE(random_state=12, ratio = 1.0)
x_train_res, y_train_res = sm.fit_sample(X_train, y_train)

clf_rf = RandomForestClassifier(n_estimators=25, random_state=12)
clf_rf.fit(x_train_res, y_train_res)

print("Validation Results")
print(clf_rf.score(X_test, y_test))
print(recall_score(y_test, clf_rf.predict(X_test), average="binary", pos_label="Yes"))
#print '\nTest Results'
#print clf_rf.score(test_features, test_target)
#print recall_score(test_target, clf_rf.predict(test_features))