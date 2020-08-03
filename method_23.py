from collections import defaultdict

def log_missing():
    # hook function
    print('key added')
    return 0


# 需求：给defaultdict传入一个产生默认值的hook，并令其统计处该字典一共遇到多少个缺失的值
# 实现方法1：使用带状态的闭包

def increment_with_report(current, increments):
    added_count = 0

    def missing():
        nonlocal added_count
        added_count += 1
        return 0

    result = defaultdict(missing, current)
    for key, amount in increments:
        result[key] += amount

    return result, added_count


# 实现方法2: 定义一个小型的类，把需要追踪的状态封装起来

class CountMissing(object):
    # 传给defaultdict的hook函数：CountMissing.missing
    # counter = CountMissing()
    # result = defaultdict(counter.missing, current)
    def __init__(self):
        self.added = 0

    def missing(self):
        self.added += 1
        return 0


# 改良后的方法2: 用__call__方法让相关对象像函数那样调用
# __call__方法表明，类的实例也可以像函数那样，在合适的时候充当某个api的参数（挂钩）
# 这个类的功能就相当于一个带状态的闭包 

class BetterCountMissing(object):
    # counter = BetterCountMissing()
    # result = defaultdict(counter, current) which relies on __call__ method
    def __init__(self):
        self.added = 0

    def __call__(self):
        self.added += 1
        return 0

# ----------------------TEST CODE------------------------
current = {'green': 12, 'blue': 3}
increments = [
    ('red', 5),
    ('blue', 17),
    ('orange', 9)
]
# result = defaultdict(log_missing, current)
# print('Before:', dict(result))
# for key, amount in increments:
#     result[key] += amount
# print('After:', dict(result)) # 会打印出两段'key added'

# def foo():
#     a = 0
#     def bar():
#         nonlocal a
#         a = 1
#     bar()
#     print(a)

# foo()

result, count = increment_with_report(current, increments)
assert count == 2

counter = BetterCountMissing()#CountMissing()
result = defaultdict(counter, current)
for key, amount in increments:
    result[key] += amount
assert counter.added == 2