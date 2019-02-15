import sys, getopt
import csv, sys, os

## COMMAND LINE PROMPT ARFFConverter.py -i Dataset.csv -o Dataset.arff

inputfile=''
outputfile=''

# Read command line args
myopts, args = getopt.getopt(sys.argv[1:],"i:o:")

input = open(inputfile);
output = open(outputfile,"w")

lastPos = output.tell()

output.write("@RELATION CO600Project\n\n\n")
count=1

for k in range(len(input.readline().strip().split(','))-1):
	output.write("@ATTRIBUTE occurences"+str(count)+" numeric\n")
	count+=1

tempClass = []
for line in input:
	tempClass.append(line.strip().split(',')[0]);
output.write("@ATTRIBUTE risky {"+','.join(tempClass)+" }\n\n\n")

output.write("@DATA \n");

input.seek(lastPos)

tempStr = []
for line in input:
	for i in range(len(line.strip().split(','))):
		if i!=0:
			tempStr.append(line.strip().split(',')[i])
		if i == len(line.strip().split(','))-1:
			tempStr.append(line.strip().split(',')[0])
			print (tempStr)
		i=i+1
	output.write(','.join(tempStr)+"\n")
	tempStr= []


output.close()
