!pip install torch --upgrade
!pip install torchtext --upgrade
!pip install torch==1.12.1 torchtext==0.13.1


import collections
from collections import Counter, OrderedDict
from torchtext.vocab import vocab 
import random 
import math

!wget https://www.gutenberg.org/files/2000/2000-0.txt
!mv "2000-0.txt" "quijote.txt"

class RandomGenerator:
  def __init__(self, sampling_weights):
    # Exclude
    self.population = list(range(1, len(sampling_weights) + 1))
    self.sampling_weights = sampling_weights
    self.candidates = []
    self.i = 0

  def draw(self):
    if self.i == len(self.candidates):
      # Cache `k` random sampling results
      self.candidates = random.choices(
          self.population, self.sampling_weights, k=10000)
      self.i = 0
    self.i += 1
    return self.candidates[self.i - 1]



def read_txt(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        raw_text = f.read()
    n_ignored=1
    oraciones=[line.split() for i, line in enumerate(raw_text.split('\n')) if i>=n_ignored]
    palabras= [palabra for line in oraciones for palabra in line]
    contar_obj= collections.Counter()
    contar_obj.update(palabras)
    ordenado_contar=sorted(contar_obj.items(),key=lambda x:x[1],reverse=True)
    od= OrderedDict(ordenado_contar)
    vocabulario= vocab(od,min_freq=10)
    n_palabras=sum(contar_obj.values())
    resultado = [[palabra for palabra in line if (random.uniform(0, 1) < math.sqrt(1e-4 / od[palabra] * n_palabras))] for line in oraciones]
    corpus= [[vocabulario[x] for x in line if vocabulario.__contains__(x)] for line in resultado if line != []]
    centros, contextos, negativos = [],[],[]
    for line in corpus:
      if len(line)< 2:
        continue
      centros += line 
      for i in range(len(line)):
        v_size= random.randint(1,5)
        indices= list(range(max(0,i-v_size),min(len(line),i+1+v_size)))
        indices.remove(i)
        contextos.append([line[j] for j in indices])
    palabras=vocabulario.get_itos()
    pesos=[contar_obj[palabras[i]]**0.75 for i in range(1,len(palabras))]
    generador= RandomGenerator(pesos)
    for k in contextos:
      negativo=[]
      while len(negativo) < len(k)*5:
        n = generador.draw()
        if n not in contextos:
          negativo.append(n)
          negativos.append(negativo)
    return negativos


g=read_txt("quijote.txt")

print(g)
