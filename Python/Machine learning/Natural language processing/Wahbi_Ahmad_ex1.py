from sys import argv
import re
from langdetect import detect
from langdetect import detect_langs


IllegalMarks = {'http:','https:',"*","@","#","^","[","]","{","}","<",">","&","r/","www.",".com",".net","//","\\"}
allowed= {'Dr.','dr.','Mr.','mr.','mrs.','Mrs.','Ms.','ms.','prof.','Prof.','&','etc.'}

#class CreateCorpus:

 #   def __init__(self, input_filename, output_dir_path):
  #      self._input = ./inputTest
   #     self._output = ./outputTest

    # Implement class here #
def deEmojify(text):
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U0001F1F2-\U0001F1F4"  # Macau flag
        u"\U0001F1E6-\U0001F1FF"  # flags
        u"\U0001F600-\U0001F64F"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U0001F1F2"
        u"\U0001F1F4"
        u"\U0001F620"
        u"\u200d"
        u"\u2640-\u2642"
        "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'',text)

if __name__ == "__main__":

    input_filename = argv[1]
    output_dir_path = argv[2]
inp = open(input_filename, "r")
fen = open(output_dir_path+"en.txt", "w")
fes = open(output_dir_path+"es.txt", "w")
fen_es = open(output_dir_path+"en_es.txt", "w")
for x in inp:
    for y in x.splitlines():
        cleanline=""
        line=deEmojify(y)
        if line!="":#The Text is split into lines with no empty lines
            num_of_tokens=0
            for word in line.split(" "):#split text into words
                cleanword=""
                allowedflag=0
                for alloweditem in allowed:
                    if alloweditem==word:
                        allowedflag=1
                if allowedflag==0:
                    for Illegal in IllegalMarks:
                        if Illegal in word:#clean illegal words (urls and emojis etc)
                            word=""
                        tokens=[word]#split word into tokens
                    tokens=re.findall(r"[\w']+|[.,!?;]", word , re.UNICODE)
                    for token in tokens:#bring original line back
                        num_of_tokens=num_of_tokens+1
                        cleanword=cleanword+token
                    if cleanword!="":
                        cleanline=cleanline+cleanword+" "
                else:
                    cleanline=cleanline+word+" "
            if num_of_tokens<4:
                cleanline=""
        if cleanline!="" and re.search('[a-zA-Z]', cleanline):
            languages=detect_langs(cleanline)
            lan={}
            for lang in languages:
                lan.update({lang.lang: lang.prob})
            en=lan.get('en')
            es=lan.get('es')
            if en!=None:
                if en>0.95:
                    fen.write(cleanline+"\n")
            else:
                if es!=None:
                    if es>0.95:
                        fes.write(cleanline+"\n")
                else:
                    if en!=None and es!=None:
                        if (en>0.6 and es>0.1) or (es>0.6 and en>0.1):
                            fen_es.write(cleanline+"\n")
fen.close()
fes.close()
fen_es.close()

    # Implement your program here

