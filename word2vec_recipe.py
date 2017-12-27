from konlpy.tag import Kkma
from konlpy.tag import Mecab
from konlpy.utils import pprint
from gensim.models import Word2Vec

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

        # ingre_tokenizer = step.split()

        mystr += ''.join(e for e in step if e.isalnum())

    return mystr

kkma = Kkma()

stopWord_Ingre = {"재료" , "계량법" , "안내" , "조금"}

''' --------------- Ingredient ---------------
for line in reader:

    ingre_tokenizer = line[4].split()

    for ingre_token in ingre_tokenizer:

        if(num_there(ingre_token)):
            mystr += ''.join(e for e in ingre_token if e.isalnum())
'''
mystr = getString("/home/gwangjik/문서/hanyang corps/데이터/만개의레시피/Text/text_recipe10000_6880650_6880700")
mystr += getString("/home/gwangjik/문서/hanyang corps/데이터/만개의레시피/Text/text_recipe10000_6880550_6880650")

print("-------------read complete-----------String length : " , len(mystr))

tokenized = kkma.pos(mystr)

sentence = kkma.sentences(mystr)

print(sentence)

print("-------------pos complete-----------all tuple length : " , len(tokenized))

print(mystr)

token_filtered = list(filter(lambda mytoken: mytoken[1] == "NNG" and not mytoken[0] in stopWord_Ingre, tokenized))
#token_filtered = list(filter(lambda mytoken: mytoken[1] == "NNG" , tokenized))

print("-------------filter complete-----------filter tuple length : " , len(token_filtered))

print(token_filtered)

embedding_model = Word2Vec(token_filtered , size=100, window = 5, min_count=2 , workers=1, iter=100, sg=1)

print("-------------word vector complete-----------")

print(embedding_model.most_similar(positive=["고기"] , topn = 5))