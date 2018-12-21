import csv

words = [] #storage of all words in CSV
words_count = [] #storage of number of times a word has been counted
reader = [] # storage of csv reader

# open data collection csv
with open ('Data-Collection.csv') as file:
    for row in csv.reader(file, delimiter=','):
        words += row
#split each cell in csv then append words
    for cell in reader:
      csv_words = cell.split(" ")
      for word in csv_words:
       words.append(word)

for word in words:
    i = words.count(word)
    words_count.append((word,i))

#output the counted words
with open('output.csv', 'w') as out:
    writer = csv.writer(out)
    writer.writerow(words_count)

#NOTE THAT THIS CODE CURRENTLY DOESNT REMOVE DUPLICATE WORDS,
#SO YOU WILL HAVE TO REMOVE DUPLICATES IN EXCEL
