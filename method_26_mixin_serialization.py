

# class ToDictMixin(object):
#     # 将内存中的Python对象转换为字典，以便将其序列化
#     def to_dict(self):
#         return self._traverse_dict(self.__dict__)

#     def _traverse_dict(self, instance_dict):
#         output = {}
#         for key, value in instance_dict.items():
#             output[key] = self._traverse(key, value)
#         return output

#     def _traverse(self, key, value):
#         if isinstance(value, ToDictMixin):
#             return value.to_dict()
#         elif isinstance(value, dict):
#             return self._traverse_dict(value)
#         elif isinstance(value, list):
#             return [self._traverse(key, i) for i in value]
#         elif hasattr(value, '__dict__'):
#             return self._traverse_dict(value.__dict__)
#         else:
#             return value
import json, pickle

class ToDictMixin(object):
    def to_dict(self):
        return self._traverse_dict(self.__dict__)

    def _traverse_dict(self, attr_dict):
        result = {}
        for key, value in attr_dict.items():
            result[key] = self._traverse(key, value)
        return result

    def _traverse(self, key, value):
        if isinstance(value, ToDictMixin): # maybe 多余？
            return value.to_dict()
        elif isinstance(value, list):
            return [self._traverse(key, i) for i in value]
        elif isinstance(value, dict):
            return self._traverse_dict(value)
        elif hasattr(value, '__dict__'):
            return self._traverse_dict(value.__dict__)
        else:
            return value # 递归的出口


class JsonMixin(object):
    # 这个Mix-in能够为任意类提供通用的json序列化功能
    # 继承这个Mix-in的条件： 1. 包含to_dict()方法； 2. __init__方法接受关键字参数
    @classmethod
    def from_json(cls, data):
        kwargs = json.loads(data)
        return cls(**kwargs)

    def to_json(self):
        return json.dumps(self.to_dict())




class BinaryTree(ToDictMixin):
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

class OtherClass(object):
    def __init__(self,x):
        self.x = x

class MyClass(ToDictMixin):
    def __init__(self, value, my_list=[], my_dict={}, my_tree=None, other_class=None):
        self.value = value
        self.my_list = my_list
        self.my_dict = my_dict
        self.my_tree = my_tree
        self.other_class = other_class

class BinaryTreeWithParent(BinaryTree):
    # 新的二叉树类添加了parent属性，为防止序列化时陷入死循环，需要override _traverse 方法
    def __init__(self, value, left=None, right=None, parent=None):
        super().__init__(value, left=left, right=right)
        self.parent = parent

    def _traverse(self, key, value):
        if isinstance(value, BinaryTreeWithParent) and key == 'parent':
            return value.value
        else:
            return super()._traverse(key, value)


class NamedSubTree(ToDictMixin):
    def __init__(self, name, tree_with_parent):
        self.name = name
        self.tree_with_parent = tree_with_parent




# ---------- TEST CODE --------

if __name__ == '__main__':
    
    tree = BinaryTree(10,
        left=BinaryTree(7),
        right=BinaryTree(13, left=BinaryTree(11)))

    my_instance = MyClass(2, [1,2], {'x':tree, 'y':2}, my_tree=tree, other_class=OtherClass(0))
    root = BinaryTreeWithParent(10)
    root.left = BinaryTreeWithParent(7, parent=root)
    root.left.right = BinaryTreeWithParent(9, parent=root.left)
    # print(root.left.value)
    # print(root.to_dict())
    # my_tree = NamedSubTree('foo', root.left.right)
    # my_se = pickle.dumps(tree)
    # with open('dump.txt', 'wb') as f:
    #     pickle.dump(my_tree, f)

    # with open('dump.txt', 'rb') as f:
    #     readout = pickle.load(f)
    tree_json = json.dumps(tree, default=lambda obj: obj.__dict__)
    def hook_function(d):
        attrs = tree.__dict__.keys()
        return BinaryTree(*[d[attr] for attr in attrs])
    tree_des = json.loads(tree_json, object_hook=hook_function)


    

    








