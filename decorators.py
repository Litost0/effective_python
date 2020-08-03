import functools, time

# def log(func):
#     def wrapper(*args, **kwargs):
#         print('Calling: %s' % func.__name__)
#         return func(*args, **kwargs)
#     return wrapper


# @log
# def function(x):
#     return x+1


# 打印函数名
def log(text):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print(text + ' ' + func.__name__)
            return func(*args, **kwargs)
        return wrapper
    return decorator

# 打印函数执行的时间
def metric(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        time_0 = time.time()
        result = func(*args, **kwargs)
        time_1 = time.time()
        print('Function: {} takes {:.2f}s'.format(func.__name__, time_1 - time_0))
        return result
    return wrapper

def record(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print('start call')
        result = func(*args, **kwargs)
        print('end call')
        return result
    return wrapper


@metric # function = metric(function)
def function(x):
    time.sleep(5)
    return x + 1


result = function(10)



