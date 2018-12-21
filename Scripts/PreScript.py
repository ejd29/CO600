import nltk
import string
import csv
import io

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize import sent_tokenize, word_tokenize

porter_stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

#contracts = ["asdaContract.txt", "lycaContract.txt", "eeContract.txt", "giffgaff.txt"]
contracts = ["asdaContract.txt"]
#contracts = ["8Contracts.txt"]

risky_sentences = []
safe_sentences = []
all_words = [] # All the words taken directly from the contracts
headers = [] # Headers for the dataset

def classifySentences():
    for n in range(len(contracts)):

        f = open(contracts[n])
        raw = f.read()

        sent_tokenize_list = sent_tokenize(raw)

        for x in range(len(sent_tokenize_list)):
            is_risky = False
            words = word_tokenize(sent_tokenize_list[x])

            for y in range(len(words)):
                all_words.append(words[y])
                if "0cf333" in words[y]:
                    is_risky = True

            if is_risky == True:
                    risky_sentences.append(words)
            else:
                    safe_sentences.append(words)

def processWords(input_data):

    single_word_list = [] #This will store each word in a single cell
    unique_words = [] #This list stores all the unique words, excluding duplicates
    filter_stemming = [] #List for Stemmer (using the porter stemmer algorithm)
    filter_lemmatizer = [] #List for Lemmatizer
    final_stem_unique = [] #Unique Stem List

    #print(input_data)

    for celem in input_data:
        try:
            nopunc = celem.translate(str.maketrans('','',string.punctuation))
            unique_words.append(nopunc)
        except:
            print("couldn't remove punctuation")

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

    final_stem_unique.sort()

    #Exclude words
    #excludeWords = ['0', '79', '800', 'EE', 'BT','cf','b','c' , 'e','f','g',''','h','ii','$','wo','nt','ip',''','gsm','iii','a','sl','dx','isl','p','k','l','n','eg','st','uptod','ait','gb','iv','v','vi',' wwwgiffgaffsimcardscouk',' examplecomgiffgaff',' giffgaffexamplecom','vii','viii','x','xi','xii', 't','cs','rd','I',' wwwicoorguk','eea','ec4a','bd','pm','dpo','s','o','iab','ga','ck','.','ag','ukon','myvm','jr','sa','bb', 79, '79']

    excludeWords= ['As', '800', 'BT', '2732', '42', '79', '0']

    for excludeWord in excludeWords:
        if excludeWord in final_stem_unique:
            final_stem_unique.remove(excludeWord);

    return final_stem_unique


#Puts list in a csv file as an excl generated file

with open('NewTest.csv', 'w') as myfile:
    classifySentences();
    headers = processWords(all_words)
    headers.append("Is_Risky?")

    wr = csv.writer(myfile, dialect='excel')
    wr.writerow(headers)
    print("File Successfully saved.")

    for sentence in risky_sentences:
        processed_sentence = processWords(sentence)
        attributes_present = []
        for attribute in headers:
            if attribute in processed_sentence:
                attributes_present.append(1)
            else:
                attributes_present.append(0)
        attributes_present[-1:] = ["Yes"]
        wr.writerow(attributes_present)

    for sentence in safe_sentences:
        processed_sentence = processWords(sentence)
        attributes_present = []
        for attribute in headers:
            if attribute in processed_sentence:
                attributes_present.append(1)
            else:
                attributes_present.append(0)
        attributes_present[-1:] = ["No"]
        wr.writerow(attributes_present)
