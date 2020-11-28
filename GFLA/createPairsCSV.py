import csv
import glob
import random

file1 = open('fasion-annotation-test.csv', 'r')
Lines = file1.readlines()
targetArray = []
for l in Lines:
    targetArray.append(l.split(":")[0])

print(targetArray[990], len(targetArray))

with open('fasion-pairs-test_styleOP.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(['', "from", "to"])
    pathFiles = glob.glob("/Users/chinmayiprasad/Documents/DeepLearning/Project/Global-Flow-Local-Attention/styleOP_images/*.jpg")
    for i in range(len(pathFiles)):
        randTargetPose = random.randint(0, len(targetArray) - 1)
        while "WOMEN" not in targetArray[randTargetPose] or "Pants" in targetArray[randTargetPose] or "Shorts" in targetArray[randTargetPose]:
            randTargetPose = random.randint(0, len(targetArray)-1)
        writer.writerow([i,pathFiles[i].split("/")[-1], targetArray[randTargetPose]])


f = open('fasion-pairs-test.csv', 'r')

line = f.readline()
line = f.readline()

# fr = open('/Users/raj/Desktop/DL - CS566/Project/test data for GCP/grabbed.csv', 'w')

find = []
while line:
    d = line.split(',')[2].strip('\n')
    find.append(d)
    line = f.readline()

# print(len(find), len(list(set(find))))
find = list(set(find))

f = open('fasion-annotation-test.csv', 'r')
line = f.readline()
line = f.readline()
s = {}
while line:
    splt = line.split(':')
    s[splt[0]] = splt[0] + ":" + splt[1] + ":" + splt[2].strip('\n')
    # print(s)
    line = f.readline()

fr = open('grabbed.csv', 'w')
for i in find:
    fr.write(s[i]+"\n")