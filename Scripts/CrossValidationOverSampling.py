import numpy as np
import pandas as pd
import math
import random
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import recall_score
from imblearn.over_sampling import SMOTE
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import precision_score
from sklearn.naive_bayes import GaussianNB
from sklearn import tree
from sklearn import svm

def floor(number, bound=1):
    return bound * math.floor(number / bound)

def randomChoiceList(oldlist, count=1):
    newlist = []

    for i in range(0,count):
        x = random.choice(oldlist)
        oldlist.remove(x)
        newlist.append(x)

    return newlist
    

def train_test_split_crossval(dataset_X, dataset_Y, test_set_used, test_examples_count):
    all_indexes = range(0, len(dataset_X))
    test_used_removed = [x for x in all_indexes if x not in test_set_used]
    #dataset_test_removed = np.delete(dataset_X, (test_set_used), axis=0) #removes rows from dataset that have already been used in another test set

    test_examples_index = randomChoiceList(test_used_removed, count=int(test_examples_count)) #indexes of new test set examples from remaining available examples
    training_set_indexes = [x for x in all_indexes if x not in test_examples_index]

    ##SANITY CHECKS##
    sanity_check_test_examples_test_used = [x for x in test_examples_index if x not in test_set_used]
    sanity_check_training_test_set = [x for x in training_set_indexes if x not in test_examples_index]

    if(len(sanity_check_training_test_set) != len(training_set_indexes)):
        print("Examples from test set are in training set")

    if(len(sanity_check_test_examples_test_used) != len(test_examples_index)):
        print("Examples from previous test sets are in current test set")

    X_train = np.delete(dataset_X, (test_examples_index), axis=0)
    Y_train = np.delete(dataset_Y, (test_examples_index), axis=0)
    X_test = np.delete(dataset_X, (training_set_indexes), axis=0)
    Y_test = np.delete(dataset_Y, (training_set_indexes), axis=0)

    test_set_used.extend(test_examples_index)

    return X_train, X_test, Y_train, Y_test, test_set_used

dataset = pd.read_csv('Dataset12Contracts.csv', ',', encoding="utf-8")
dataset_columns = len(dataset.columns)
dataset_attributes_X = dataset.columns.values[0:dataset_columns-1].tolist()
dataset_attribute_Y = dataset.columns.values[dataset_columns-1:dataset_columns].tolist()

examples_target = floor(len(dataset), bound=10)
rows_to_drop = len(dataset) - examples_target

dataset.drop(dataset.tail(rows_to_drop).index,inplace=True)

dataset_X = dataset[dataset_attributes_X].as_matrix()
#dataset_Y = pd.get_dummies(dataset[dataset_attribute_Y]).as_matrix()
dataset_Y = dataset[dataset_attribute_Y].as_matrix()

print(dataset_X.shape)
#dataset_X = np.delete(dataset_X, (0), axis=0)
print(dataset_X.shape)

recall_score_pos_sum = 0
recall_score_neg_sum = 0
precision_score_pos_sum = 0
precision_score_neg_sum = 0
test_set_used = []

for i in range(0,10):
    X_train, X_test, y_train, y_test, test_set_used = train_test_split_crossval(dataset_X, dataset_Y, test_set_used, examples_target/10)
    sm = SMOTE(random_state=12, ratio = 1.0)
    x_train_res, y_train_res = sm.fit_sample(X_train, y_train)
    #clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(33,2), random_state=12)
    #clf = RandomForestClassifier(n_estimators=25, random_state=12)
    clf = GaussianNB()
    #clf = tree.DecisionTreeClassifier()
    #clf = svm.SVC(gamma='scale')
    clf.fit(x_train_res, y_train_res)

    recall_score_pos = recall_score(y_test, clf.predict(X_test), average="binary", pos_label="Yes")
    recall_score_neg = recall_score(y_test, clf.predict(X_test), average="binary", pos_label="No")
    precision_score_pos = precision_score(y_test, clf.predict(X_test), average='binary', pos_label="Yes")
    precision_score_neg = precision_score(y_test, clf.predict(X_test), average='binary', pos_label="No")

    recall_score_pos_sum += recall_score_pos
    recall_score_neg_sum += recall_score_neg
    precision_score_pos_sum += precision_score_pos
    precision_score_neg_sum += precision_score_neg

    print(recall_score_pos)
    print(recall_score_neg)
    print(precision_score_pos)
    print(precision_score_neg)

print("Final accuracy results: ")
recall_pos_avg = recall_score_pos_sum/10
recall_neg_avg = recall_score_neg_sum/10
precision_pos_avg = precision_score_pos_sum/10
precision_neg_avg = precision_score_neg_sum/10
print(recall_pos_avg)
print(recall_neg_avg)
print(precision_pos_avg)
print(precision_neg_avg)








    
