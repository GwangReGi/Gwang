
# coding: utf-8

# In[64]:


from konlpy.tag import Kkma
from gensim.models import Word2Vec
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import csv;


# In[65]:


import matplotlib.font_manager as fm
font_location = "/home/gwangjik/문서/hanyang corps/라이브러리/NanumBarunGothic.ttf"
font_name = fm.FontProperties(fname=font_location).get_name()
plt.rc('font', family=font_name)


# In[66]:


def num_there(s):
    return not(any(i.isdigit() for i in s))


# In[67]:


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


# In[68]:


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


# In[69]:


kkma = Kkma()

stopWord_Ingre = {"재료" , "계량법" , "안내" , "조금"}


# In[113]:


mystr = getString("/home/gwangjik/문서/hanyang corps/데이터/만개의레시피/Text/text_recipe10000_6879000_6880000")
mystr += getString("/home/gwangjik/문서/hanyang corps/데이터/만개의레시피/Text/text_recipe10000_6870000_6871000")


# In[ ]:


tokenized = kkma.pos(mystr)


# In[ ]:


token_filtered = list(filter(lambda mytoken: mytoken[1] == "NNG" or mytoken == "NNG" or mytoken == "NNB" and not mytoken[0] in stopWord_Ingre, tokenized))


# In[ ]:


embedding_model = Word2Vec(token_filtered , size=10, window = 3, min_count=0 , workers=3, iter=10, sg=1)


# In[ ]:


labels = []
tokens = []


# In[ ]:


for word in embedding_model.wv.vocab:
        tokens.append(embedding_model.wv.word_vec(word))
        labels.append(word)


# In[ ]:


tsne_model = TSNE(learning_rate=100)


# In[ ]:


new_values = tsne_model.fit_transform(tokens)


# In[ ]:


x = []
y = []
for value in new_values:
    x.append(value[0])
    y.append(value[1])


# In[ ]:


for i in range(len(x)):
    plt.scatter(x[i], y[i])
    plt.annotate(labels[i],
                 xy=(x[i], y[i]),
                 xytext=(5, 2),
                 textcoords='offset points',
                 ha='right',
                 va='bottom')


# In[ ]:


plt.show()


# In[ ]:


print(embedding_model.wv.similar_by_word("버섯"))

