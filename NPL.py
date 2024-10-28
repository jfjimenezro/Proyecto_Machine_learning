pip install torch --upgrade
pip install torchtext --upgrade
pip install torch==1.12.1 torchtext==0.13.1

import collections
from collections import Counter, OrderedDict
from torchtext.vocab import vocab 
import random 
import math


!wget https://www.gutenberg.org/files/225/225-0.txt
!mv "225-0.txt" "cien_anos_soledad.txt"


def read_txt(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        raw_text = f.read()
    oraciones=[line.split() for i, line in enumerate(raw_text.split('\n'))]
    palabras= [palabra for line in oraciones for palabra in line]
    contar_obj= collections.Counter()
    contar_obj.update(palabras)
    ordenado_contar=sorted(contar_obj.items(),key=lambda x:x[1],reverse=True)
    od= OrderedDict(ordenado_contar)
    vocabulario= vocab(od,min_freq=10)
    n_palabras=sum(contar_obj.values())
    
    resultado = [[palabra for palabra in line if (random.uniform(0, 1) < math.sqrt(1e-4 / od[palabra] * n_palabras))] for line in oraciones]
    
    return resultado 


print(read_txt("cien_anos_soledad.txt"))
