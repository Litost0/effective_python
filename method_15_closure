



def sort_priority(values, group):

    flag = False # 返回一个状态，表示values中有没有group中的元素

    def helper(x):
        nonlocal flag # 少用
        if x in group:
            flag = True
            return (0, x)
        return (1, x)

    values.sort(key=helper)
    return flag


class Sorter(object):
    def __init__(self, group):
        self.group = group
        self.found = False

    def __call__(self, x):
        if x in self.group:
            self.found = True
            return (0, x)
        return (1, x)



# ------- TEST CODE -------

if __name__ == '__main__':

    numbers = [8, 1, 9, 5, 4, 7, 6]
    group = [1, 2, 9]
    has_group_number = sort_priority(numbers, group)

    sorter = Sorter(group)
    numbers.sort(key=sorter)
    print(sorter.found)
    print(numbers)
    print(sorter(7))

