import collections


class SimpleGradebook(object):

    def __init__(self):
        self._grades = {}

    def add_student(self, name):
        self._grades[name] = []

    def report_grade(self, name, score):
        self._grades[name].append(score)

    def average_grade(self, name):
        grades = self._grades[name]
        return sum(grades) / len(grades)

# 按科目记录成绩

class BySubjectGradebook(object):

    def __init__(self):
        self._grades = {}

    def add_student(self, name):
        self._grades[name] = {} # 分科目 {name:{subject:[grade,],},}

    def report_grade(self, name, subject, grade):
        by_subject = self._grades[name]
        grade_list = by_subject.setdefault(subject, [])
        grade_list.append(grade)

    def average_grade(self, name):
        by_subject = self._grades[name]
        total, count = 0, 0
        for grades in by_subject.values():
            total += sum(grades)
            count += len(grades)
        return total / count


# 每次成绩的权重不一样
# 随着需求越来越复杂，依赖字典来维护gradebook越来越困难
# 用来保存程序状态的数据结构过于复杂，就应该将其拆解成类，以便提供更明确的借口

# namedtuple可以很容易地定义出精简而不可变的数据类

Grade = collections.namedtuple('Grade', ('score', 'weight'))

class Subject(object):

    '''表示科目的类，包含一系列考试成绩'''

    def __init__(self):
        self._grades = [] # list of namedtuples

    def report_grade(self, score, weight):
        self._grades.append(Grade(score, weight))

    def average_grade(self):
        total, total_weight = 0, 0
        for grade in self._grades:
            total += grade.score * grade.weight
            total_weight += grade.weight
        return total / total_weight


class Student(object):

    '''表示学生的类，包含学生学习的课程'''

    def __init__(self):
        self._subject = {}

    def subject(self, name):



# ------------------TEST CODE---------------------

if __name__ == '__main__':
    
    # book = SimpleGradebook()
    # book.add_student('Fubuki')
    # book.report_grade('Fubuki', 75)
    # book.report_grade('Fubuki', 85)
    # assert book.average_grade('Fubuki') == 80

    # book = BySubjectGradebook()
    # book.add_student('Fubuki')
    # book.report_grade('Fubuki', 'English', 90)
    # book.report_grade('Fubuki', 'English', 80)
    # book.report_grade('Fubuki', 'Math', 70)
    # assert book.average_grade('Fubuki') == 80

    # Vtb = collections.namedtuple('vtb', ('name', 'race'))
    # fubuki = Vtb('Fubuki', 'kizune')
    # print(fubuki.race)

