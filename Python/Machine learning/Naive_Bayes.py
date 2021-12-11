import pandas as pd
import math
from collections import defaultdict

Alpha=0.2

def training():
    data=pd.read_csv("data_train.csv").dropna()
    spamSum,nonSpamSum=0,0
    non_spam_vocabulary, spam_vocabulary=defaultdict(lambda:Alpha),defaultdict(lambda:Alpha)#First time seeing the word it's value is 1, in training it becomes 2, in test it remains 1 (smoothing)
    for row in data.iloc:#making the vocabularies
        for word in row["email"].split():
            if row["label"]==1: 
                spam_vocabulary[word]=spam_vocabulary[word]+1
                spamSum=spamSum+1
            else: 
                non_spam_vocabulary[word]=non_spam_vocabulary[word]+1
                nonSpamSum=nonSpamSum+1
    return  non_spam_vocabulary, spam_vocabulary,spamSum,nonSpamSum

def testing(non_spam_vocabulary, spam_vocabulary,spamSum,nonSpamSum):
    tests=pd.read_csv("data_test.csv").dropna()
    corrctAnswers=0
    for test in tests.iloc:
        probSpam,probNonSpam=1,1
        for word in test["email"].split():
            probSpam=probSpam+(math.log(spam_vocabulary[word]/spamSum))#Use log so the result won't be so small that it's replaced with zero, also x1-<y=>log(x)<log(y)
            probNonSpam=probNonSpam+(math.log(non_spam_vocabulary[word]/nonSpamSum))
        if ((probSpam>probNonSpam)and(test["label"]==1))or((probNonSpam>probSpam)and(test["label"]==0)):
            corrctAnswers=corrctAnswers+1
    return corrctAnswers,len(tests["email"])


if __name__=='__main__':
    non_spam_vocabulary, spam_vocabulary,spamSum,nonSpamSum=training()#returns vocabularies and number of words 

    corrctAnswers,testsNum=testing(non_spam_vocabulary, spam_vocabulary,spamSum,nonSpamSum)
    

    print(str((corrctAnswers/testsNum)*100)+"%")


    

    