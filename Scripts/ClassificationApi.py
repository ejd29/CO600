import flask
from flask import request
from flask import jsonify
from flask_cors import CORS
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import recall_score
from imblearn.over_sampling import SMOTE
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import SnowballStemmer
from sklearn.neural_network import MLPClassifier
import sys

app = flask.Flask(__name__)
app.config["DEBUG"] = False
CORS(app)

snowball_stemmer = SnowballStemmer('english')

dataset = pd.read_csv('Dataset12Contracts.csv', ',', encoding='utf-8')
dataset_columns = len(dataset.columns)
dataset_attributes_X = dataset.columns.values[0:dataset_columns-1].tolist()
dataset_attribute_Y = dataset.columns.values[dataset_columns-1:dataset_columns].tolist()

dataset_X = dataset[dataset_attributes_X].as_matrix()
#dataset_Y = pd.get_dummies(dataset[dataset_attribute_Y]).as_matrix()
dataset_Y = dataset[dataset_attribute_Y].as_matrix()

X_train, X_test, y_train, y_test = train_test_split(dataset_X, dataset_Y, test_size=0.2, random_state=12)

sm = SMOTE(random_state=12, ratio = 1.0)
x_train_res, y_train_res = sm.fit_sample(X_train, y_train)

clf = RandomForestClassifier(n_estimators=25, random_state=12)
clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(30,), random_state=12)
clf.fit(x_train_res, y_train_res)

#testVar = "I shouldn't be this value"

#def onLoad():
#   global testVar
#   testVar = "I should be this value"

#onLoad()

@app.route('/', methods=['GET'])
def home():
        req_data = request.get_json()
        print(req_data)

        language = req_data['language']
        framework = req_data['framework']

        return '''
                The language value is: {}
                The framework value is: {}
                '''.format(language, framework)

@app.route('/ModelTest', methods=['POST'])
def ModelTest():
        global clf
        risky_statement_locations = []
        risky_statements = []
        req_data = request.get_json()

        document = req_data['document'].replace('\n', ' ')
        sent_tokenize_list = sent_tokenize(document)

        for sentence in sent_tokenize_list:
                sentence_stemmed = []

                words = word_tokenize(sentence)
                for word in words:
                        sentence_stemmed.append(snowball_stemmer.stem(word))

                attribute_sequence = ConvertSentencetoAttributeSequence(sentence_stemmed)
                predicted_class = clf.predict(attribute_sequence)

                if predicted_class == "Yes":
                        beginning_of_sentence = document.find(sentence)
                        length_of_sentence = len(sentence)
                        end_of_sentence = beginning_of_sentence + length_of_sentence
                        risky_statement_locations.append(beginning_of_sentence)
                        risky_statement_locations.append(end_of_sentence)
                        risky_statements.append(sentence)


        return jsonify(rsl=risky_statement_locations, rs=risky_statements)


def ConvertSentencetoAttributeSequence(sentence):
        attributes_present = [[]]
        words = sentence

        for attribute in dataset_attributes_X:
                if attribute in words:
                        attrib_count = words.count(attribute)
                        attributes_present[0].append(attrib_count)
                else:
                        attributes_present[0].append(0)

        print(attributes_present)

        return attributes_present

app.run()
