import csv
import nltk
import io

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize import sent_tokenize, word_tokenize

porter_stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

input_data = [] #This will store all the words/sentences from the csv file
single_word_list = [] #This will store each word in a single cell
unique_words = [] #This list stores all the unique words, excluding duplicates
filter_stemming = [] #List for Stemmer (using the porter stemmer algorithm)
filter_lemmatizer = [] #List for Lemmatizer
final__stem_unique = [] #Unique Stem List

#This opens the csv file and stores data into the list
try:
    with open('Data-Collection.csv') as csv_file:
        for row in csv.reader(csv_file, delimiter=',',quoting=csv.QUOTE_NONE):
            input_data += row
except:
    print("Unable to process 'Data-Collection'. Please close the file if it is open.")

#checks the list for sentences and splits them into words -> stores to a new list
for cel_elem in input_data:
    second_list = cel_elem.split()
    for new_cel_elem in second_list:
        single_word_list.append(new_cel_elem)


for elem in single_word_list:
    if elem not in unique_words:
        for repl in ((".",""),("\"",""),("(",""), (")",""), (";",""), ("¬","")):
            elem = elem.replace(*repl)
        unique_words.append(elem)

#Removes stop words
filter_stop_list = unique_words[:]
for elemw in unique_words:
    if elemw in stopwords.words('english'):
        filter_stop_list.remove(elemw)

filter_nostopwords = [elemxx for elemxx in filter_stop_list if elemxx]

final_filter = [elemx for elemx in unique_words if elemx]

for fn in filter_nostopwords:
    filter_stemming.append(porter_stemmer.stem(fn))

for fl in filter_nostopwords:
    filter_lemmatizer.append(lemmatizer.lemmatize(fl))

#Removing duplicates in stemming
for elem in filter_stemming:
    if elem not in final_stem_unique:
        final_stem_unique.append(elem)

#Puts list in a csv file as an excl generated file
try:
    with open('NewTest.csv', 'w') as myfile:
        wr = csv.writer(myfile, dialect='excel')
        wr.writerow(filter_nostopwords)
        #wr.writerow(filter_lemmatizer)
        print("File Successfully saved.")
except:
    print("Unable to save file. Please close the 'NewTest' file if it is opened.")

#print(len(unique_words), " Unique words")
#print(len(filter_nostopwords), " No Stop words")
#print(len(filter_stemming), " Stemming")
#print(len(filter_lemmatizer), " Lemmatizer words")
