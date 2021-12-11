from gensim.scripts.glove2word2vec import glove2word2vec
from sys import argv
from gensim.models import KeyedVectors
import re
import random
import numpy as np
from sklearn.decomposition import PCA  
import matplotlib.pyplot as plt 
 # Load the GolVe to vector files, blacken after loading (or do it in a separate Python file):
# glove2word2vec(<downloaded text file_300>, <full path vector filename for your use for glove_file_50>)
# glove2word2vec(<downloaded text file_50>, <full path vector filename for your use for glove_file_300>)
# pre_trained_model_50 = KeyedVectors.load_word2vec_format(glove_file_50, binary=False)
# pre_trained_model_300 = KeyedVectors.load_word2vec_format(glove_file_300, binary=False)
# pre_trained_model_50.save(<full path vector filename for your use, end with '.kv'>)
# pre_trained_model_300.save(<full path vector filename for your use, end with '.kv'>)

common=["I","he","she","the","these","no","yes","that","I'm","be","to","and","a","in","have"]
def chosen_weight(word):
    res=1
    if len(word)>3:
        res=res+1
    if word not in common:
        res+2
    return res
# Implement your code here #


if __name__ == "__main__":
    en_corpus = argv[1]         # English corpus, text file
    glove_file_50 = argv[2]     # 50-vector, kv file
    glove_file_300 = argv[3]    # 300-vector, kv file
    song_lyrics = argv[4]       # Lyrics, text file
    output_file = argv[5]       # Output, text file

    corpus = open(en_corpus, "r")
    glove_file_50=open(glove_file_50,"r")
    glove_file_300=open(glove_file_300,"r")
    lyrics=open(song_lyrics,"r")
    output=open(output_file,"w")
    # Building the models:
    pre_trained_model_50 = KeyedVectors.load_word2vec_format(glove_file_50, binary=False)
    pre_trained_model_300 = KeyedVectors.load_word2vec_format(glove_file_300, binary=False)
   # pre_trained_model_50.save(glove_file_50)
   # pre_trained_model_300.save(glove_file_300)
    # Biden's Tweets:
    tweets = ["America, I'm honored that you have chosen me to lead our great country. The work ahead of us will be hard, but I promise you this: I will be a President for all Americans — whether you voted for me or not. I will keep the faith that you have placed in me.",
              "If we act now on the American Jobs Plan, in 50 years, people will look back and say this was the moment that America won the future.",
              "Gun violence in this country is an epidemic — and it’s long past time Congress take action. It matters whether you continue to wear a mask. It matters whether you continue to socially distance. It matters whether you wash your hands. It all matters and can help save lives.",
              "If there’s one message I want to cut through to everyone in this country, it’s this: The vaccines are safe. For yourself, your family, your community, our country — take the vaccine when it’s your turn and available. That’s how we’ll beat this pandemic.",
              "Today, America is officially back in the Paris Climate Agreement. Let’s get to work.",
              "Today, in a bipartisan vote, the House voted to impeach and hold President Trump accountable. Now, the process continues to the Senate—and I hope they’ll deal with their Constitutional responsibilities on impeachment while also working on the other urgent business of this nation.",
              "The work of the next four years must be the restoration of democracy and the recovery of respect for the rule of law, and the renewal of a politics that’s about solving problems — not stoking the flames of hate and chaos.",
              "America is so much better than what we’re seeing today.",
              "Here’s my promise to you: I’ll be a president for all Americans. Whether you voted for me or not, I’ll wake up every single morning and work to make your life better.",
              "We can save 60,000-100,000 lives in the weeks and months ahead if we step up together. Wear a mask. Stay socially distanced. Avoid large indoor gatherings. Each of us has a duty to do what we can to protect ourselves, our families, and our fellow Americans."]

    # Implement your program here 
    #part A---------------------------------------------------------------------------------------------
    #1
    list1=['boy','lion','leg','cat','python','microsoft','league','ronaldo','fire','open']
    list2=['girl','tiger','hand','dog','c++','apple','cup','messi','water','close']
    
    #2
    list11=['day','liquid','barcelona','bull','war']
    list12=['night','water','madrid','cow','peace']
    list21=['dark','ice','football','female','ally']
    list22=['light','solid','golf','male','enemy']
    results=[]
    pre_trained_model_list=[pre_trained_model_50,pre_trained_model_300]
    for i in range(0,2):
        pre_trained_model=pre_trained_model_list[i]
        output.write("\n\n\n\n=== "+str(50+i*250)+" Word Model ===")
        output.write("Word Pairs and Distance:\n")
        for i in range(0,10):
            output.write(str(i+1)+". "+list1[i]+"-"+list2[i]+":"+str(pre_trained_model.similarity(list1[i],list2[i])))
        output.write("\n\nAnalogies:\n")
        for i in range(0,5):
            output.write(str(i+1)+". "+list11[i]+" : "+list12[i]+" , "+list21[i]+" : "+list22[i])

        for i in range(0,5):
            results.append(pre_trained_model.most_similar(positive=[list11[i],list21[i]],negative=[list22[i]],topn=1))
        
        output.write("\n\nMost Similar:\n")
        for i in range(0,5):
            output.write(str(i+1)+". "+list11[i]+" + "+list21[i]+" - "+list22[i]+" = "+results[i][0][0])

        output.write("\n\nDistance:\n")
        for i in range(0,5):
            output.write(str(i+1)+". "+list12[i]+" - "+results[i][0][0]+" : "+str(pre_trained_model.similarity(list12[i],results[i][0][0])))
            #output.write("the word is "+word[i][0]+" the distance is "+str(pre_trained_model_50.similarity(list12[i],word[i][0]))+"\n\n")

    output.write("-*-*-*-\n\n\n")
    #part B---------------------------------------------------------------------------------------------
    tweetslines=[]
    WordsToChange=["you","all","placed","american","epidemic","mask","socially","your","save","safe","vaccine","beat","back","work","trump","responsibilities","law","better","all","morning","save","mask","socially","avoid","americans"]
    for tweet in tweets:#split tweets into lines
        for line in tweet.split("."):
            tweetslines.append(line)
    bigram={}
    trigram={}
    bi_number_of_words=0
    tri_number_of_words=0
    for x in corpus:#Making the grams 
        for y in x.splitlines():
            y=" thestartofsentence "+y.lower()+" theendofsentence"
            biprev=""
            trifirst=""
            trisecond=""
            for word in y.split("."):
                tokens=re.findall(r"[\w']+|[.,!?;]", word , re.UNICODE)
                for token in tokens:#bring original line back
                    token=token.lower()
                    if (re.search('[a-zA-Z]', token) or token=='thestartofsentence' or token=='theendofsentence') and  not re.search('[0-9]', token):#if word contains letters (no need for numbers and punctuation marks)
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
    #End of making the grams
    Illegal=[',','.','!','?',';','thestartofsentence','theendofsentence']
    tokens=[]
    tri_words=[]
    bi_words=[]
    i=0
    places=[]
    for sentence in tweetslines:#check triwords
        temp_bi=[]
        if sentence !="":
            sentence=sentence.lower()
            tokens=re.findall(r"[\w']+|[.,!?;]", sentence , re.UNICODE)
            index=tokens.index(WordsToChange[i])
            candlist=pre_trained_model_50.similar_by_word(WordsToChange[i],topn=10)
            triword=""
            biword1=""
            biword2=""
            if(index!=0 and index!=len(tokens)-1):#get triword
                if((tokens[index-1] not in Illegal)and(tokens[index+1] not in Illegal)):
                    triword=tokens[index-1]+" "+tokens[index]+" "+tokens[index+1]
                    biword1=tokens[index-1]+" "+tokens[index]
                    biword2=tokens[index]+" "+tokens[index+1]
            else:
                if(index==0):
                     if((tokens[index+1] not in Illegal)and(tokens[index+2] not in Illegal)):
                         triword=tokens[index]+" "+tokens[index+1]+" "+tokens[index+2]
                         biword1=tokens[index]+" "+tokens[index+1]
                if(index==len(tokens)-1):
                    if((tokens[index-1] not in Illegal)and(tokens[index-2] not in Illegal)):
                        triword=tokens[index-2]+" "+tokens[index-1]+" "+tokens[index]
                        biword1=tokens[index-1]+" "+tokens[index]
            tri_words.append(triword)
            temp_bi.append(biword1)
            temp_bi.append(biword2)
            bi_words.append(temp_bi)
            i=i+1
    max_array=[]
    max_words=[""]*len(WordsToChange)
    i=0
    similar_words=[]
    for word in tri_words:
        similar_words=pre_trained_model_50.most_similar(positive=WordsToChange[i],topn=10)
        max=0
        for sim_word in similar_words:
            newword=word.replace(WordsToChange[i],sim_word[0])
            if newword in trigram:
                if(max<trigram[newword]):
                    max=trigram[newword]
                    max_words[i]=sim_word[0]
        max_array.append(max)
        i=i+1
    for k in range(0,len(WordsToChange)-1):
        similar_words=pre_trained_model_50.most_similar(positive=WordsToChange[k],topn=10)
        for sim_word in similar_words:
            max=0
            temp_max=0
            if max_array[k]==0:
                for bi_word in bi_words[k]:
                    if(bi_word in bigram):
                     temp_max=temp_max+bigram[bi_word]
                if max<temp_max:
                    max=temp_max
                    max_words[k]=sim_word[0]
        if max_array[k]==0:
            max_words[k]=similar_words[0][0]

    i=0
    output.write("=== New Tweets ===\n")
    for sentence in tweetslines:
        if sentence!="":
            output.write(str(i+1)+". "+sentence.lower().replace(WordsToChange[i],max_words[i])+"\n")
            i=i+1

    #Part C-------------------------------------------------------------------------------------------
    #    output.write(pre_trained_model_50.get_vector("car"))
    pca = PCA(n_components=2)
    songs=[]
    writers=[]
    vectors_art=[]
    vectors_random=[]
    vectors_chosen=[]
    number_of_words_in_lyrics=0
    for line in lyrics.read().split("\n"):
        if "===" in line:
            if number_of_words_in_lyrics!=0:
                songs.append(song_name)
                writers.append(writer_name)
                init_vec_1=np.divide(init_vec_1,number_of_words_in_lyrics)
                init_vec_random=np.divide(init_vec_random,number_of_words_in_lyrics)
                init_vec_chosen=np.divide(init_vec_chosen,number_of_words_in_lyrics)
                vectors_art.append(init_vec_1)
                vectors_random.append(init_vec_random)
                vectors_chosen.append(init_vec_chosen)
            init_vec_1=1
            init_vec_random=1
            init_vec_chosen=1
            number_of_words_in_lyrics=0
            song_name=line.replace("===","")
            song_name=song_name.replace(" ","")
        else:
            if "== " in line:
                writer_name=line.replace("==","")
                writer_name=line.replace(" ","")
            else:
                if line!="":
                    for word in line.split(" "):
                        if word in pre_trained_model_300:
                            number_of_words_in_lyrics=number_of_words_in_lyrics+1
                            init_vec_1=np.add(init_vec_1,np.multiply(pre_trained_model_50.get_vector(word),1))
                            init_vec_random=np.add(init_vec_random,np.multiply(pre_trained_model_300.get_vector(word),random.randint(1,4)))
                            init_vec_chosen=np.add(init_vec_chosen,np.multiply(pre_trained_model_300.get_vector(word),chosen_weight(word)))
    

    vectors_art= pca.fit_transform(vectors_art)
    vectors_random=pca.fit_transform(vectors_random)
    vectors_chosen=pca.fit_transform(vectors_chosen)
                        
    the_Xs_art=[]
    the_Ys_art=[]
    the_Xs_rand=[]
    the_Ys_rand=[]
    the_Xs_chosen=[]
    the_Ys_chosen=[]
    for i in range(0,len(vectors_art)):
        the_Xs_art.append(vectors_art[i][0])
        the_Ys_art.append(vectors_art[i][1])
        the_Xs_rand.append(vectors_random[i][0])
        the_Ys_rand.append(vectors_random[i][1])
        the_Xs_chosen.append(vectors_chosen[i][0])
        the_Ys_chosen.append(vectors_chosen[i][1])
    
    plt.scatter(the_Xs_art,the_Ys_art,c="blue")
    plt.scatter(the_Xs_rand,the_Ys_rand,c="green")
    plt.scatter(the_Xs_chosen,the_Ys_chosen,c="red")

    plt.title('Arithmetic average wight func\n')
    for i in range(0,len(the_Xs_art)):
        plt.annotate(songs[i]+"\n"+writers[i]+"\n"+"artmetic"+"\n" , (the_Xs_art[i],the_Ys_art[i]))
        plt.annotate(songs[i]+"\n"+writers[i]+"\n"+"random"+"\n" , (the_Xs_rand[i],the_Ys_rand[i]))
        plt.annotate(songs[i]+"\n"+writers[i]+"\n"+"chosen"+"\n" , (the_Xs_chosen[i],the_Ys_chosen[i]))
    plt.show() 



    corpus.close() 
    glove_file_50.close()
    glove_file_300.close()
    lyrics.close()
    output.close()
