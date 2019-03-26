import numpy as np
import pandas as pd
import csv
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import recall_score
from imblearn.over_sampling import SMOTE
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import precision_score
from sklearn.naive_bayes import GaussianNB
from sklearn import svm

dataset = pd.read_csv('Dataset12Contracts.csv', ',', encoding="utf-8")
dataset_columns = len(dataset.columns)
dataset_attributes_X = dataset.columns.values[0:dataset_columns-1].tolist()
dataset_attribute_Y = dataset.columns.values[dataset_columns-1:dataset_columns].tolist()

dataset_X = dataset[dataset_attributes_X].as_matrix()
#dataset_Y = pd.get_dummies(dataset[dataset_attribute_Y]).as_matrix()
dataset_Y = dataset[dataset_attribute_Y].as_matrix()

print(dataset_X.shape)
print(dataset_Y)

X_train, X_test, y_train, y_test = train_test_split(dataset_X, dataset_Y, test_size=0.2, random_state=12)

sm = SMOTE(random_state=12, ratio = 1.0)
x_train_res, y_train_res = sm.fit_sample(X_train, y_train)

'''
#clf = RandomForestClassifier(n_estimators=25, random_state=12)
#clf = GaussianNB()
clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(33,2), random_state=12)
#clf.fit(X_train, y_train)
clf.fit(x_train_res, y_train_res)
print(recall_score(y_test, clf.predict(X_test), average="binary", pos_label="Yes"))
print(precision_score(y_test, clf.predict(X_test), average='binary', pos_label="Yes"))
print(recall_score(y_test, clf.predict(X_test), average="binary", pos_label="No"))
print(precision_score(y_test, clf.predict(X_test), average='binary', pos_label="No"))
'''

with open('AutoMLResults.csv', 'w', newline='') as myfile:

    wr = csv.writer(myfile, dialect='excel')
    wr.writerow(['hidden layers', 'hidden units', 'accuracy', 'recall_risky', 'precision_risky', 'recall_safe', 'precision_safe'])

    for n in range(1,3):
        for i in range(1,41): 
            clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(i,n), random_state=12)
            clf.fit(x_train_res, y_train_res)
            print("Validation results for %s hidden units with %s hidden layer(s)" % (i, n))

            accuracy = clf.score(X_test, y_test)
            recall_pos = recall_score(y_test, clf.predict(X_test), average="binary", pos_label="Yes")
            precision_pos = precision_score(y_test, clf.predict(X_test), average='binary', pos_label="Yes")
            recall_neg = recall_score(y_test, clf.predict(X_test), average="binary", pos_label="No")
            precision_neg = precision_score(y_test, clf.predict(X_test), average='binary', pos_label="No")

            print(accuracy)
            print(recall_pos)
            print(precision_pos)
            print(recall_neg)
            print(precision_neg)
            print("\n")

            wr.writerow([n, i, accuracy, recall_pos, precision_pos, recall_neg, precision_neg])

print("AutoML Results created successfully")

#clf = svm.SVC(gamma='scale')


#print("Validation Results")
#print(clf.score(X_test, y_test))
#print(recall_score(y_test, clf.predict(X_test), average="binary", pos_label="Yes"))
#print '\nTest Results'
#print clf_rf.score(test_features, test_target)
#print recall_score(test_target, clf_rf.predict(test_features))