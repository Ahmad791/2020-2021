from sys import argv
import re
import random
# Implement your code here #


if __name__ == "__main__":

    en_corpus = argv[1]
    es_corpus = argv[2]
    output_file = argv[3]
    phrases = ["You never know what you're gonna get",
               "Keep your friends close, but your enemies closer",
               "I've got a feeling we're not in Kansas anymore",
               "Quiero respirar tu cuello despacito",
               "Me gusta la moto, me gustas tú",
               "Dale a tu cuerpo alegría Macarena"]

    # Implement your main program here #

en = open(en_corpus, "r")
es = open(es_corpus, "r")
corps=[en,es]
output = open(output_file+"output.txt", "w")
unigram={}
bigram={}
trigram={}
en_unigram={}
en_bigram={}
en_trigram={}
es_unigram={}
es_bigram={}
es_trigram={}
en_uni_number_of_words=0
en_bi_number_of_words=0
en_tri_number_of_words=0
es_uni_number_of_words=0
es_bi_number_of_words=0
es_tri_number_of_words=0
uni_number_of_words=0
bi_number_of_words=0
tri_number_of_words=0
for corp in corps:
    unigram={}
    bigram={}
    trigram={}
    for x in corp:#making the grams 
        for y in x.splitlines():
            y=" thestartofsentence "+y.lower()+" theendofsentence"
            biprev=""
            trifirst=""
            trisecond=""
            for word in y.split(" "):
                tokens=re.findall(r"[\w']+|[.,!?;]", word , re.UNICODE)
                for token in tokens:#bring original line back
                    token=token.lower()
                    if (re.search('[a-zA-Z]', token) or token=='thestartofsentence' or token=='theendofsentence') and  not re.search('[0-9]', token):#if word contains letters (no need for numbers and punctuation marks)
                        uni_number_of_words=uni_number_of_words+1
                        if trifirst!="":#trigram
                            if trisecond!="":
                                tri_number_of_words=tri_number_of_words+1
                                triword=trisecond+" "+trifirst+" "+token
                                if triword in trigram:
                                    trigram[triword]=trigram[triword]+1
                                else:
                                    trigram[triword]=1
                            trisecond=trifirst
                        trifirst=token
                        if biprev!="":#bigram
                            bi_number_of_words=bi_number_of_words+1
                            biword=biprev+" "+token
                            if biword in bigram:
                                bigram[biword]=bigram[biword]+1
                            else:
                                    bigram[biword]=2
                        biprev=token
                        if token in unigram:#unigram
                            unigram[token]=unigram[token]+1
                        else:
                            unigram[token]=2
    if corps.index(corp)==0:
        en_unigram=unigram
        en_bigram=bigram
        en_trigram=trigram
        en_uni_number_of_words=uni_number_of_words
        en_bi_number_of_words=bi_number_of_words
        en_tri_number_of_words=tri_number_of_words
    else:
        es_unigram=unigram
        es_bigram=bigram
        es_trigram=trigram
        es_uni_number_of_words=uni_number_of_words
        es_bi_number_of_words=bi_number_of_words
        es_tri_number_of_words=tri_number_of_words

# end ofmaking the grams----------------------------------------------------------------------------
for line in phrases:
    output.write("\n"+"for sentence number "+str(phrases.index(line)+1)+"\n")
#uni section
    line=line.lower()
    for i in range(2):
        probability=1
        if i==0:
            unigram=en_unigram
            uni_number_of_words=en_uni_number_of_words
        else:
            unigram=es_unigram
            uni_number_of_words=es_uni_number_of_words
        for word in line.split(" "):
            if word in unigram:
                probability=probability*((unigram[word])/uni_number_of_words)
            else: 
                probability=probability*(1/uni_number_of_words)
        if i==0:
            output.write("\n"+"Unigram Model: "+str(probability)+" for english ")
        else:
            output.write("\n"+str(probability)+" for spanish ")
#bi section
    for i in range(2):
        probability=1
        if i==0:
            unigram=en_unigram
            bigram=en_bigram
            uni_number_of_words=en_uni_number_of_words
            bi_number_of_words=en_bi_number_of_words
        else:
            unigram=es_unigram
            bigram=es_bigram
            uni_number_of_words=es_uni_number_of_words
            bi_number_of_words=es_bi_number_of_words
        biprev=""
        biword=""
        probability=1
        for word in line.split(" "):
            if biprev!="":
                biword=biprev+" "+word
                if biprev in unigram and biword in bigram:
                    probability=probability*((bigram[biword])/(unigram[biprev]+bi_number_of_words))
                else: 
                    if biprev in unigram:
                        probability=probability*(1/(unigram[biprev]+bi_number_of_words))
                    else:
                        probability=probability*(1/bi_number_of_words)
            biprev=word
        if i==0:
            output.write("\n"+"Bigram Model: "+str(probability)+" for english ")
        else:
            output.write("\n"+str(probability)+" for spanish ")
#tri section
    for i in range(2):
        probability=1
        if i==0:
            unigram=en_unigram
            bigram=en_bigram
            trigram=en_trigram
            uni_number_of_words=en_uni_number_of_words
            bi_number_of_words=en_bi_number_of_words
            tri_number_of_words=en_tri_number_of_words
        else:
            unigram=es_unigram
            bigram=es_bigram
            trigram=en_trigram
            uni_number_of_words=es_uni_number_of_words
            bi_number_of_words=es_bi_number_of_words
            tri_number_of_words=es_tri_number_of_words
        trifirst=""
        trisecond=""
        triword=""
        probability=1
        for word in line.split(" "):
            interpolation=0
            if trifirst!="":
                if trisecond!="":
                    prevbiword=trisecond+" "+trifirst
                    biword=trifirst+" "+word
                    triword=trisecond+" "+trifirst+" "+word
                    if prevbiword in bigram:#calculate the tri prob
                        if triword in trigram:
                            interpolation=interpolation+0.8*(trigram[triword]/(bigram[prevbiword]+tri_number_of_words))
                        else:
                            interpolation=interpolation+0.8*(1/(bigram[prevbiword]+tri_number_of_words))
                    else:
                        interpolation=interpolation+0.8*(1/(tri_number_of_words))
                    if trifirst in unigram:#claculat the bi prob
                        if biword in bigram:
                            interpolation=interpolation+0.15*(bigram[biword]/(unigram[trifirst]+bi_number_of_words))
                        else:
                            interpolation=interpolation+0.15*(1/(unigram[trifirst]+bi_number_of_words))
                    else:
                        interpolation=interpolation+0.15*(1/(bi_number_of_words))
                    if word in unigram:#calculate the uni prob
                        interpolation=interpolation+0.05*(unigram[word]/(+uni_number_of_words))
                    else: 
                        interpolation=interpolation+0.05*(1/(uni_number_of_words))
                    probability=probability*interpolation
                trisecond=trifirst
            trifirst=word
        if i==0:
            output.write("\n"+"Trigram Model: "+str(probability)+" for english ")
        else:
            output.write("\n"+str(probability)+" for spanish \n")
#first section end ------------------------------------------------------------------------
#Unigram model
output.write("\n"+"Unigram model in english dataset")
unigram_list=list(en_unigram)
bigram_list=list(en_bigram)
trigram_list=list(en_trigram)

for i in range (3):
    length=random.randint(4,15)
    sentence="thestartofsentence"
    for j in range (length):
        next_word_index=random.randint(0,len(unigram_list))
        word=unigram_list[next_word_index]
        sentence=sentence+" "+word
        if(word=="theendofsentence"):
            break
    output.write("\n"+sentence)

output.write("\n"+"Bigram model in english dataset")
for i in range (3):
    length=random.randint(4,15)
    sentence="thestartofsentence"
    prevbi="thestartofsentence"
    for j in range (length):
        word=""
        next_word_index=random.randint(0,len(bigram_list))
        for index in range(next_word_index,len(bigram_list)):
            cand_word=bigram_list[index]
            #output.write("\n"+"candword is "+cand_word)
            if prevbi==cand_word.split(" ")[0]:
                word=cand_word.split(" ")[1]
                break
        if word=="":
            for index2 in range(0,next_word_index):
                cand_word=bigram_list[index2]
                if prevbi in cand_word.split(" ")[0]:
                    word=cand_word.split(" ")[1]
                    break
        sentence=sentence+" "+word
        if(word=="theendofsentence"):
            break
        prevbi=word
    output.write("\n"+sentence)

output.write("\n"+"trigram model in english dataset")
for i in range (3):
    first_tri=""
    second_tri=""
    length=random.randint(4,15)
    word=""
    first_word=random.randint(0,len(trigram_list))
    for index in range(first_word,len(trigram_list)):
        cand_word=trigram_list[index]
        #output.write("\n"+"candword is "+cand_word)
        if "thestartofsentence" in cand_word:
            word=cand_word
            second_tri=cand_word.split(" ")[1]
            first_tri=cand_word.split(" ")[2]
            break
    if word=="":
        for index in range(0,first_word):
            cand_word=trigram_list[index]
            if "thestartofsentence" in cand_word:
                word=cand_word
                second_tri=cand_word.split(" ")[1]
                first_tri=cand_word.split(" ")[2]
                break

    sentence=word+" "
    for j in range (length):
        prevtri=second_tri+" "+first_tri
        word=""
        next_word_index=random.randint(0,len(trigram_list))
        cand_word=trigram_list[next_word_index]
        for index in range(next_word_index,len(trigram_list)):
            cand_word=trigram_list[index]
            #output.write("\n"+"candword is "+cand_word)
            if prevtri==(cand_word.split(" ")[0]+" "+ cand_word.split(" ")[1]):
                word=cand_word.split(" ")[2]
                break
        if word=="":
            for index in range(0,next_word_index):
                cand_word=trigram_list[index]
                if prevtri in cand_word:
                    word=cand_word.split(" ")[2]
                    break
        sentence=sentence+" "+word
        if(word=="theendofsentence"):
            break
        second_tri=first_tri
        first_tri=word+" "
    output.write("\n"+sentence)

#Unigram model
output.write("\n"+"Unigram model in bilingual dataset")
unigram_list.extend(list(es_unigram))
bigram_list.extend(list(es_bigram))
trigram_list.extend(list(en_trigram))

for i in range (3):
    length=random.randint(4,15)
    sentence="thestartofsentence"
    for j in range (length):
        next_word_index=random.randint(0,len(unigram_list))
        word=unigram_list[next_word_index]
        sentence=sentence+" "+word
        if(word=="theendofsentence"):
            break
    output.write("\n"+sentence)

output.write("\n"+"Bigram model in bilingual dataset")
for i in range (3):
    length=random.randint(4,15)
    sentence="thestartofsentence"
    prevbi="thestartofsentence"
    for j in range (length):
        word=""
        next_word_index=random.randint(0,len(bigram_list))
        for index in range(next_word_index,len(bigram_list)):
            cand_word=bigram_list[index]
            #output.write("\n"+"candword is "+cand_word)
            if prevbi==cand_word.split(" ")[0]:
                word=cand_word.split(" ")[1]
                break
        if word=="":
            for index2 in range(0,next_word_index):
                cand_word=bigram_list[index2]
                if prevbi in cand_word.split(" ")[0]:
                    word=cand_word.split(" ")[1]
                    break
        sentence=sentence+" "+word
        if(word=="theendofsentence"):
            break
        prevbi=word
    output.write("\n"+sentence)

output.write("\n"+"trigram model in bilingual dataset")
for i in range (3):
    first_tri=""
    second_tri=""
    length=random.randint(6,15)
    word=""
    first_word=random.randint(0,len(trigram_list))
    for index in range(first_word,len(trigram_list)):
        cand_word=trigram_list[index]
        #output.write("\n"+"candword is "+cand_word)
        if "thestartofsentence" in cand_word:
            word=cand_word
            second_tri=cand_word.split(" ")[1]
            first_tri=cand_word.split(" ")[2]
            break
    if word=="":
        for index in range(0,first_word):
            cand_word=trigram_list[index]
            if "thestartofsentence" in cand_word:
                word=cand_word
                second_tri=cand_word.split(" ")[1]
                first_tri=cand_word.split(" ")[2]
                break

    sentence=word+" "
    for j in range (length):
        prevtri=second_tri+" "+first_tri
        word=""
        next_word_index=random.randint(0,len(trigram_list))
        cand_word=trigram_list[next_word_index]
        for index in range(next_word_index,len(trigram_list)):
            cand_word=trigram_list[index]
            #output.write("\n"+"candword is "+cand_word)
            if prevtri==(cand_word.split(" ")[0]+" "+ cand_word.split(" ")[1]):
                word=cand_word.split(" ")[2]
                break
        if word=="":
            for index in range(0,next_word_index):
                cand_word=trigram_list[index]
                if prevtri in cand_word:
                    word=cand_word.split(" ")[2]
                    break
        sentence=sentence+" "+word
        if(word=="theendofsentence"):
            break
        second_tri=first_tri
        first_tri=word+" "
    output.write("\n"+sentence)
en.close()
es.close()
output.close()