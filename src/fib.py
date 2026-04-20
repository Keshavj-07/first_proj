def fib(x):
    if x % 1 != 0 or x < 0:
        raise NotImplementedError('fib only defined on non-negative integers.')
    cache = {}
    def fib_inner(x):
        nonlocal cache
        if x in cache:
            return cache[x]
        if x == 0:
            return 0
        elif x == 1:
            return 1
        else:
            val = fib_inner(x - 1) + fib_inner(x - 2)
            cache[x] = val
            return val
    return fib_inner(x)