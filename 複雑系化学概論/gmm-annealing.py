#積分を最大化する方針で、MixtureModelを書いてみた。
#一筋縄では行かないことがよくわかった。

from math import *
def normaldistrib(x,mu,sigma):
    return exp(-0.5*((x-mu)/sigma)**2) / (sqrt(2.0*pi)* sigma)

def dNoverdmu(x,mu,sigma):
    return (x-mu)/sigma**2 * normaldistrib(x,mu,sigma)

def dNoverdsigma(x,mu,sigma):
    return normaldistrib(x,mu,sigma)*((x-mu)**2 - sigma**2)/sigma**3

def gamma2w( gamma ):
    sum = 0.0
    w = [0.0] * len(gamma)
    for i in range(len(gamma)):
        w[i] = exp(gamma[i])
        sum += w[i]
    for i in range(len(gamma)):
        w[i] /= sum
    return w


def boxmuller(mu,sigma):
    alpha = random()
    beta = random()
    return sigma*sqrt(-2.0*log(alpha))*sin(2*pi*beta)+mu

mu = [0.8,1.2]
sigma = [0.3,0.3]
gamma = [1.0,1.0]
#const
dmix = [1.0,-1.0]
bin = dict()
raw = []
count = 0

speed(10)

for i in range(100):
    x = boxmuller(1,0.1)
    raw.append(x) 
    x = int(x*100)*0.01
    if bin.has_key(x):
        bin[x] += 1
    else:
        bin[x] = 1
    count += 1
    
    
for i in range(100):
    x = boxmuller(1.3,0.2)
    raw.append(x)
    x = int(x*100)*0.01
    if bin.has_key(x):
        bin[x] += 1
    else:
        bin[x] = 1
    count += 1


def draw():
    ddg = [0.0,0.0]
    ddm = [0.0,0.0]
    dds = [0.0,0.0]
    w = gamma2w( gamma )
    for k in range(len(mu)):
        for b in raw:
            sumq = 0.0
            sumr = w[k] * normaldistrib(b,mu[k],sigma[k])
            for j in range(len(mu)):
                sumq += w[j]      * normaldistrib(b,mu[j],sigma[j])
                sumr -= w[k]*w[j] * normaldistrib(b,mu[j],sigma[j])
            ddg[k] += sumr / sumq
            ddm[k] += w[k] * dNoverdmu(b,mu[k],sigma[k]) / sumq
            dds[k] += w[k] * dNoverdsigma(b,mu[k],sigma[k]) / sumq
    for k in range(len(mu)):
        gamma[k] += ddg[k]*0.0003
        mu[k]    += ddm[k]*0.0001
        sigma[k] += dds[k]*0.0001
    #杉山将先生のレジュメを参考に最急降下法を作ったが、うまくいかない。なぜだあ。
    print mu,w,sigma
    stroke(0.5)
    nofill()
    for b in bin.keys():
        line(b*100,200,b*100,(200-bin[b]*100*50/count))
    stroke(1,0,0)
    nofill()
    beginpath(0,200.0)
    for i in range(len(mu)):
        for b in sorted(bin.keys()):
            lineto(b*100,(200-50*w[i]*normaldistrib(b,mu[i],sigma[i])))
    endpath()
    stroke(0,0,1)
    beginpath(0,200.0)
    for b in sorted(bin.keys()):
        s = 0.0
        for i in range(len(mu)):
            s += w[i]*normaldistrib(b,mu[i],sigma[i])
        lineto(b*100,(200-50*s))
    endpath()
                   