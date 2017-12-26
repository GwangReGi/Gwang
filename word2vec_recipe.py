from konlpy.tag import Kkma
from konlpy.tag import Mecab
from konlpy.utils import pprint
from gensim.models import Word2Vec

import csv;

def num_there(s):
    return not(any(i.isdigit() for i in s))


kkma = Kkma()


fr = open("/home/gwangjik/문서/hanyang corps/데이터/만개의레시피/Text/text_recipe10000_6880650_6880700", 'r', encoding='utf-8')
reader = csv.reader(fr)

mystr = ""

stopWord_Ingre = {"재료" , "계량법" , "안내" , "조금"}


for line in reader:

    ingre_tokenizer = line[4].split()

    for ingre_token in ingre_tokenizer:

        if(num_there(ingre_token)):
            mystr += ''.join(e for e in ingre_token if e.isalnum())

tokenized = kkma.pos(mystr)

token = "iniate"

print(mystr)


token_filtered = list(filter(lambda mytoken: mytoken[1] == "NNG" and not mytoken[0] in stopWord_Ingre, tokenized))
#token_filtered = list(filter(lambda mytoken: mytoken[1] == "NNG" , tokenized))

print(token_filtered)

embedding_model = Word2Vec(token_filtered , size=10, window = 2, min_count=2 , workers=1, iter=100, sg=1)

print(embedding_model.most_similar(positive=["고추"] , topn = 5))