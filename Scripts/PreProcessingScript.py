import nltk
import string
import csv
import io
import re

from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from nltk.tokenize import sent_tokenize, word_tokenize

snowball_stemmer = SnowballStemmer('english')
stop_words = set(stopwords.words('english'))

#contracts = ["asdaContract.txt", "lycaContract.txt", "eeContract.txt", "giffgaff.txt"]
#contracts = ["asdaContract.txt"]
contracts = ["8Contracts.txt"]

risky_sentences = []
safe_sentences = []
all_words = {} # All the words taken directly from the contracts
headers = [] # Headers for the dataset


def classifySentences():
    for n in range(len(contracts)):

        f = open(contracts[n])
        raw = f.read()

        raw = raw.replace('\n', '. ')

        sent_tokenize_list = sent_tokenize(raw)

        for x in range(len(sent_tokenize_list)):
            is_risky = False
            words = word_tokenize(sent_tokenize_list[x])

            for y in range(len(words)):

                if words[y] in all_words:
                    all_words[words[y]] += 1
                else:
                    all_words[words[y]] = 1

                if "0cf333" in words[y]:
                    is_risky = True

            if is_risky == True:
                    risky_sentences.append(words)
            else:
                    safe_sentences.append(words)

def processWords(input_data, headers=False):


    input_data_array = input_data

    if(headers==True):
        #remove words with less than three words
        input_data_array = []
        input_data = {key:val for key, val in input_data.items() if val > 15}

        for key in input_data:
            input_data_array.append(key)

    unique_words = [] #This list stores all the unique words, excluding duplicates
    filter_stemming = [] #List for Stemmer (using the porter stemmer algorithm)
    final_stem_unique = [] #Unique Stem List
    filter_stop_list = [] #List with no stopwords

    filter_no_num = []#List with no numbers
    filter_non_empty = []#List with no empty elements
    filter_exclude = []#List of excluded words removed

    #Removes punctuation
    for input_data_elem in input_data_array:
        try:
            nopunc = input_data_elem.translate(str.maketrans('','',string.punctuation))
            unique_words.append(nopunc)
        except:
            print("couldn't remove punctuation")

    #Removes stop words
    for unique_words_elem in unique_words:
        if unique_words_elem.lower() not in stopwords.words('english'):
            filter_stop_list.append(unique_words_elem.lower())

    #Exclude words
    excludeWords = ['EE', 'BT','cf','b','c', 'e','f','g','h','ii','$','wo','nt','gsm','iii','a','sl','dx','isl','p','k','l','n','eg','st','uptod','ait','gb','iv','v','vi','examplecomgiffgaff', 'giffgaffexamplecom','vii','viii','x','xi','xii', 'ix', 'ie', 'ii', 't','cs','rd','I','wwwicoorguk','eea','ec4a','bd','pm','dpo','s','o','iab','ga','ck','ag','ukon','myvm','jr','sa','bb', 'andor', '0cf333', 'cf333', 'upon', 'us', 'third', 'onto', 'one', 'third', 'one', 'first', 'two', 'for', 'within', 'without', 'wo', 'wwwallaboutcookiesorg', 'wwwcallcreditcoukcrain', 'wwwcifasorguk', 'wwwequifaxcoukcrain', 'wwwexperiancoukcrain', 'wwwgiffgaffcomsupportask', 'wwwgiffgaffsimcardscouk', 'wwwicoorguk', 'wwwlycamobilecoukencontactus', 'wwwlycamobilecoukenroamingwithineucountries', 'wwwo2coukcookiepolicy', 'wwwombudsmanservicesorg', 'wwwthreecouk', 'wwwthreecouktermsconditionspaymandpayg', 'wwwvirginmediacom', 'wwwyouronlinechoiceseu', 'ukonly', 'ub8', 'thereof', 'th', 'hereinafter', 'h', 'g', 'ga', 'euus', 'etc', 'bb', 'although', '·', '–', '‘', '’', '“', '”', '•', 'also', 'asda', 'ensur', 'get', 'giffgaff', 'giffgaffcom', 'let', 'like', 'lycamobil', 'make', 'mean', 'o2', 'see', 'tesco', 'three', 'take', 'virgin']

    filter_exclude = [word for word in filter_stop_list if word not in excludeWords]

    #Removes numbers
    for checknum in filter_exclude:
        if not checknum.isdigit():
            filter_no_num.append(checknum.lstrip('£0123456789'));

    #Apply Snowball Stemming
    for fn in filter_no_num:
        filter_stemming.append(snowball_stemmer.stem(fn))

    #Removing duplicates in stemming
    for elem in filter_stemming:
        if elem not in filter_non_empty:
            filter_non_empty.append(elem)

    #Removes empty elements
    final_stem_unique = [elemxx for elemxx in filter_non_empty if elemxx]

    #Sorts all words in order
    final_stem_unique.sort()

    return final_stem_unique


#Puts list in a csv file as an excl generated file

with open('Dataset.csv', 'w', newline='') as myfile:
    print("Creating Dataset...")
    classifySentences()

    headers = processWords(all_words, True)

    headers.append("Is_Risky?")

    wr = csv.writer(myfile, dialect='excel')
    wr.writerow(headers)


    for sentence in risky_sentences:
        processed_sentence = processWords(sentence)

        attributes_dict = {}

        attributes_present = []
        for attribute in headers:
            if attribute in processed_sentence:
                #count how many times attribute appears in sentence
                #attrib_count = sentence.count(attribute)
                attributes_present.append(1)
                if attribute in attributes_dict:
                    attributes_dict[attribute] += 1
                else:
                    attributes_dict[attribute] = 1
            else:
                attributes_present.append(0)
        attributes_present[-1:] = ["Yes"]
        wr.writerow(attributes_present)

    for sentence in safe_sentences:
        processed_sentence = processWords(sentence)
        attributes_present = []
        for attribute in headers:
            if attribute in processed_sentence:
                #count how many times attribute appears in sentence
                #attrib_count = sentence.count(attribute)
                attributes_present.append(1)
                if attribute in attributes_dict:
                    attributes_dict[attribute] += 1
                else:
                    attributes_dict[attribute] = 1
            else:
                attributes_present.append(0)
        attributes_present[-1:] = ["No"]
        wr.writerow(attributes_present)
    
    wr.writerow(attributes_dict.values())

    print("Dataset successfully created and saved.")
