from konlpy.tag import Kkma
from konlpy.tag import Mecab
from konlpy.utils import pprint
from gensim.models import Word2Vec
import numpy as np
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import csv;

def num_there(s):
    return not(any(i.isdigit() for i in s))

def getString(filename):

    fr = open(filename , 'r', encoding='utf-8')
    reader = csv.reader(fr)

    mystr = ""

    for line in reader:

        step = ""

        for i in range(9, len(line)):
            step += line[i]
            step += ' '

        # ingre_tokenizer = step.split()

        mystr += ''.join(e for e in step if e == ' ' or e == '\n' or e.isalnum())
        mystr += ' '

    return mystr


def tsne_plot(model):
    #"Creates and TSNE model and plots it"
    labels = []
    tokens = []

    for word in model.wv.vocab:
        tokens.append(model[word])
        labels.append(word)

    tsne_model = TSNE(perplexity=40, n_components=2, init='pca', n_iter=2500, random_state=23)
    new_values = tsne_model.fit_transform(tokens)

    x = []
    y = []
    for value in new_values:
        x.append(value[0])
        y.append(value[1])

    plt.figure(figsize=(16, 16))

    for i in range(len(x)):
        plt.scatter(x[i], y[i])
        plt.annotate(labels[i],
                     xy=(x[i], y[i]),
                     xytext=(5, 2),
                     textcoords='offset points',
                     ha='right',
                     va='bottom')
    plt.show()


kkma = Kkma()

stopWord_Ingre = {"재료" , "계량법" , "안내" , "조금"}

''' --------------- Ingredient ---------------
for line in reader:

    ingre_tokenizer = line[4].split()

    for ingre_token in ingre_tokenizer:

        if(num_there(ingre_token)):
            mystr += ''.join(e for e in ingre_token if e.isalnum())
'''

mystr = getString("/home/gwangjik/문서/hanyang corps/데이터/만개의레시피/Text/text_recipe10000_6880815_6880816")
#mystr = getString("/home/gwangjik/문서/hanyang corps/데이터/만개의레시피/Text/text_recipe10000_6880650_6880700")
#mystr += getString("/home/gwangjik/문서/hanyang corps/데이터/만개의레시피/Text/text_recipe10000_6880550_6880650")

print("-------------read complete-----------String length : " , len(mystr))

tokenized = kkma.pos(mystr)

#sentence = kkma.sentences(mystr)

#print(sentence)


print("-------------pos complete-----------all tuple length : " , len(tokenized))

print(mystr)

token_filtered = list(filter(lambda mytoken: mytoken[1] == "NNG" or mytoken == "NNG" or mytoken == "NNB" and not mytoken[0] in stopWord_Ingre, tokenized))
#token_filtered = list(filter(lambda mytoken: mytoken[1] == "NNG" , tokenized))

print("-------------filter complete-----------filter tuple length : " , len(token_filtered))

print(token_filtered)

embedding_model = Word2Vec(token_filtered , size=10, window = 3, min_count=0 , workers=1, iter=10, sg=1)

print("-------------word vector complete-----------")

print(embedding_model.most_similar(positive=["고구마"] , topn = 5))

print(embedding_model.wv.vocab)
print(embedding_model.wv.word_vec())


#tsne_plot(embedding_model)
