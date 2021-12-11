from sys import argv
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from langdetect import detect
from sklearn import neighbors
from sklearn.model_selection import train_test_split
from sklearn.metrics import plot_confusion_matrix,classification_report
from sklearn.ensemble import RandomForestClassifier
#from sklearn.metrics import classification_report,plot_confusion_matrix
# Implement your code here #


class Classifier:

    def __init__(self, corpus_filename, output_filename, english_filename, spanish_filename):
        self._corpus_file = corpus_filename
        self._output_file = output_filename
        self._english_file = english_filename
        self._spanish_file = spanish_filename

        # Implement your class here #
names=["facebook","youtube","twitter","windows","apple","disney","tesla","bitcoin","reddit"]
short=["y","o","ir","es","e"]# y=and / o=or / ir=to go / es=it is / e=and
def get_lang(word):#detect language function
    is_eng=0
    is_esp=0
    if word in eng_dict:
        is_eng=1
    if word in esp_dict:
        is_esp=1
    lan=is_eng+is_esp*10
    if lan==0:
        landetect=detect(word)
        lan=(landetect=="eng")+(landetect=="esp")*10
        if lan==0:
            lan=0
    return lan

def get_vic(word,prevword):
    reslist=""
    if prevword==" ":
        reslist=reslist+"1"
    else:
        reslist=reslist+"0"
    if prevword!=" " and re.search('[A-Z]', word[0]):
        reslist=reslist+",1"
    else:
        reslist=reslist+",0"
    if prevword==",":
        reslist=reslist+",1"
    else:
        reslist=reslist+",0"
    if word.lower() in short:
        reslist=reslist+",1"
    else:
        reslist=reslist+",0"
    if word.lower() in names:
        reslist=reslist+",1"
    else:
        reslist=reslist+",0"
    return reslist

if __name__ == '__main__':
    input_path = argv[1]
    output_path = argv[2]
    english_dict_file = argv[3]
    spanish_dict_file = argv[4]

    cs_cls = Classifier(input_path, output_path, english_dict_file, spanish_dict_file)

input_file = open(input_path, "r")
output_file = open(output_path, "w")
data_file = open("data.txt", "w")
eng_dict = open(english_dict_file, "r").readlines()
esp_dict = open(spanish_dict_file, "r").readlines()
eng_dict = [word[:-1] for word in eng_dict]
esp_dict = [word[:-1] for word in esp_dict]
result=0
data_file.write("FW,CW,AS,IS,IN,RES\n")
#end of preparing files 
for line in input_file:
    line=line.lower()
    list1 = []
    res_vic=""
    prevlan=0#0 is english 1 spanish
    firstword=line.split(None, 1)[0]
    if re.search('[a-zA-Z]', firstword):
        prevlan=get_lang(firstword)
    else:
        curlan=0
    prevtoken=" "
    for token in line.split(" "):
        if re.search('[a-zA-Z]', token):#if it's a word (contains letters)
           curlan=get_lang(token)
        else:
            curlan=0
        #print("current token is "+token+" and curlan is "+str(curlan)+" and prevlan is "+str(prevlan))
        if curlan==0 or curlan==11 or curlan==prevlan or prevlan==0 or prevlan==11:
            result=0
        else:
            result=1
        if re.search('[a-zA-Z]', token):
            prevlan=curlan
            res_vic=get_vic(token,prevtoken)
            res_vic=res_vic+","+str(result)
            data_file.write(res_vic+"\n")
        prevtoken=token

output_file.write("The features are:\n1. First word in line.\n2.Not first word in line and first letter is capital (name).\n3.Comes after ','\n4. Word in Spanish is shorter than in english (in blacklist)\n5. Is a known company/website name.\n")

#now to do the comparison

data = pd.read_csv('data.txt')
x = np.array(data.drop(['RES'],1))
y = np.array(data['RES'])

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3)

KNC=neighbors.KNeighborsClassifier()
KNC.fit(x_train,y_train)
prediction = KNC.predict(x_test)
output_file.write("KNeighborsClassifier\n")
output_file.write(classification_report(y_test, prediction))
plot_confusion_matrix(KNC,x_test, y_test)
plt.show()
output_file.write("\nRandomForest\n")
RFC = RandomForestClassifier(max_depth=2)
RFC.fit(x_train, y_train)
prediction = RFC.predict(x_test)
output_file.write(classification_report(y_test, prediction))
plot_confusion_matrix(RFC,x_test, y_test)
plt.show()