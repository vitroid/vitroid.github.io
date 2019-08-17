import types

def sfind(C, values, fromend=False):
    """
    Given:
    C: a sequence or a iterator
    values: a collection of values to be found, or a function accepting single argument.
    fromend=False: search from end.
    
    Returns:
    An iterator returning indexes.
    """
    f = lambda x:x in values
    if isinstance(values, (types.FunctionType, types.BuiltinFunctionType, types.MethodType, types.BuiltinMethodType)):
        f = values
    found = []
    if fromend:
        C = reversed(C)
    for i,x in enumerate(C):
        if f(x):
            if fromend:
                yield -i-1
            else:
                yield i

def test():
    C = [3,1,4,1,5,9,2,6,5,3,5,8,9,7,9,3,2,3,8,4,6,2,6,4,3,3,8,3,2,7,9,5,0]
    print(tuple(sfind(C, (1,))))
    print(tuple(sfind(C, lambda x:x==1)))
    print(list(sfind(C, (1,3))))
    print(list(sfind(C, lambda x:x in (1,3))))
    print(list(sfind(C, (1,3), fromend=True)))

if __name__ == "__main__":
    test()
