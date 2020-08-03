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
        self._grades = [] # list of namedtuples [(score, weight), ]

    def report_grade(self, score, weight):
        # 为课程添加一个成绩
        self._grades.append(Grade(score, weight))

    def average_grade(self):
        # 这一科成绩的平均分
        total, total_weight = 0, 0
        for grade in self._grades:
            total += grade.score * grade.weight
            total_weight += grade.weight
        return total / total_weight


class Student(object):

    '''表示学生的类，包含学生学习的课程'''

    def __init__(self):
        self._subjects = {} # {name: Subject, }

    def subject(self, name):
        '''返回该学生某一个课程的信息，若没有这个课程，新建一个课程类'''
        if name not in self._subjects:
            self._subjects[name] = Subject()
        return self._subjects[name]

    def average_grade(self):
        # 所有成绩的平均分
        total, count = 0, 0
        for subject in self._subjects.values():
            total += subject.average_grade()
            count += 1
        return total / count


class Gradebook(object):

    '''包含所有学生考试成绩的容器类，以学生的名字为键，并且可以动态添加学生'''

    def __init__(self):
        self._students = {}

    def student(self, name):
        if name not in self._students:
            self._students[name] = Student()
        return self._students[name]




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
    book = Gradebook()
    fubuki = book.student('Shirakami Fubuki')
    math = fubuki.subject('Math')
    math.report_grade(80, 0.1)

    print(fubuki.average_grade())

