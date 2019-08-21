---
---
    from sympy.ntheory.primetest import isprime
    queue = []
    
    def CutOffPrime(n, digits):
        for i in range(1,10):
            x = i*10**digits + n
            if isprime(x):
                queue.append([x, digits+1])
    
    CutOffPrime(0,0)
    while len(queue) >0:
        x, d = queue.pop(0)
        print(x,d)
        CutOffPrime(x,d)
## Linked from

* [TruncatablePrimes](TruncatablePrimes.md)


----
[Edit](https://github.com/vitroid/vitroid.github.io/edit/master/MD/TruncatablePrimes.md)
