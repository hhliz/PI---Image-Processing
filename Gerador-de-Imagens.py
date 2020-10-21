"""
NOME: LIZ HUANCAPAZA HILASACA
ANO: 2020
TRABALHO: "Gerador de Imagens"
"""

#import matplotlib.pyplot as plt
import numpy as np
import imageio
import sys
import math
import random

#normaliza os pixels na faixa 0 - 65535
def normalize(img):
    imax = np.max(img)
    
    imin = 0.0
    
    img = (img - imin)/((imax-imin))
    img = (img*65535.0).astype(np.float32)
    
    return img

#normaliza os pixels na faixa 0 - 255
def normalize255(img):
    imax = np.max(img)
   
    imin = 0.0
    
    img = (img - imin)/((imax-imin))
    img = (img*255).astype(np.uint8)

    return img

#funcao 1 x+y   
def f1(f, C, Q, S):
    for x in range (C):
        for y in range (C):
            f[x][y] = (x+y)

    return f

#funcao 2 sin
def f2(f, C, Q, S):
    Q = float(Q)
    for x in range (C):
        for y in range (C):
            f[x][y] = math.fabs(math.sin(x/Q) + math.sin(y/Q))

    return f

#funcao 3 quad
def f3(f, C, Q, S):
    Q = float(Q)
    for x in range (C):
        for y in range (C):
            f[x][y] = abs( (x/Q) - math.sqrt(y/Q) )

    return f

#funcao 4 rand
def f4(f, C, Q, S):
    S = float(S)    
    #inicializar a semente S
    random.seed(S)
    for x in range (C):
        for y in range (C):
            #gera numeros aleatorios uniformes entre 0 e 1
            f[x][y] = float(random.uniform(0.0, 1.0))

    return f

#funcao 4 randomwalk
def f5(f, C, Q, S):
    S = float(S)    
    Q = float(Q)
    C = float(C)
    
    #inicializar a semente S
    random.seed(S)

    x = 0
    y = 0
    #estabelece o primeiro pixel como 1
    f[x][y] = float(1.0)
    for i in range (int(1+(C*C)/2)):
      
        dx = random.randint(-1, 1)
        x = int((x+dx) % C)
    
        f[x][y] = (1.0)
        
        dy = random.randint(-1, 1)
        y = int((y+dy) % C)
    
        f[x][y] = (1.0)

    return f

#rotea para as 5 funcoes que criam a imagem
def f(C, f_i, Q, S):
    switch_case = {
            1 : f1,
            2 : f2,
            3 : f3,
            4 : f4,
            5 : f5
    }
    fm = np.zeros(shape=(int(C),int(C)), dtype=np.float32)
    return switch_case[f_i](fm, C, Q, S)

#quantizacao da imagem f empregando os B bits menos significativos
def quantizacao(f, B):
    
    f = normalize255(f)
    f = f.astype(np.uint8)
    s = f.shape
    N = s[0]
    for i in range (N):
        for j in range (N):
            v =  int(f[i, j])
            f[i, j] = (v >> (8 - B))

    return f

#gerar uma amostra da imagem de NxN de comprimento
def amostragem(f, N):
    s = f.shape
    C = s[0]
    d = 0
    if N>0:
        d = int(C/(N))

    g = np.zeros(shape=(N,N), dtype=np.float32)


    for i in range (N):
        for j in range (N):
            pix = -1.0
           
            for x in range((i*d), (i*d)+d):
                for y in range((j*d), (j*d)+d):
                  
                    if x<C and y<C:
                       
                        if f[x][y]>pix:
                            pix = f[x][y]

            #atualizar na nova imagem g
            g[i][j] = pix

    return g

#cria uma amostragem g da imagem f, e tambem a quantizaca
def g(f, N, B):
    
    
    f = normalize(f)
    
    g = amostragem(f, N)
    
    g = normalize255(g)
    
    g = quantizacao(g, B)
    
    return g

#comparacao de images 
def RMSE(g, R_i):
    
    filename = str(R_i).rstrip()
    R = np.load(filename)
    s = R.shape
    n = s[0]
    err = 0.0
    for x in range (n):
        for y in range (n):
            b = int(g[x][y]) - int(R[x][y])
            err = err+(b*b)

    #err = (1.0/(n*n))*err
    return math.sqrt(err)

def main(R_i, C_i, f_i, Q_i, N_i, B_i, S_i):
    #cria a imagem de cena f
    f_o = f(C_i, f_i, Q_i, S_i)
    # cria a imagem de amostragem g e a quantizacao da mesma imagem
    g_o = g(f_o, N_i, B_i)

    r = RMSE(g_o, R_i)
    
    
    return r
    
#inicio
if __name__ == "__main__":
    
    R_i = str(input()).rstrip()
    C_i = int(input())
    f_i = int(input())
    Q_i = int(input())
    N_i = int(input())
    B_i = int(input())
    S_i = int(input())

    err = 0.0
    err = main(R_i, C_i, f_i, Q_i, N_i, B_i, S_i)
    err = format(err, '.4f')
    print (err)
  


