# 用纯属性取代get和set方法
class Resistor(object):
    def __init__(self, ohms):
        self.ohms = ohms
        self.voltage = 0
        self.current = 0


class VoltageResistance(Resistor):
    def __init__(self, ohms):
        super().__init__(ohms)
        self._voltage = 0


    @property
    def voltage(self):
        return self._voltage

    @voltage.setter
    def voltage(self, voltage):
        self._voltage = voltage
        self.current = self._voltage / self.ohms


class BoundedResistance(Resistor):
    def __init__(self, ohms):
        super().__init__(ohms)

    @property
    def ohms(self):
        return self._ohms

    @ohms.setter
    def ohms(self, ohms):
        if ohms <= 0:
            raise ValueError('%f ohms must be > 0' % ohms)
        self._ohms = ohms

    @ohms.getter
    def ohms(self):
        # ... 一般不在getter里面修改其他属性的值
        return self._ohms

class FixedResistance(Resistor):
    def __init__(self, ohms):
        super().__init__(ohms)

    @property
    def ohms(self):
        return self._ohms

    @ohms.setter
    def ohms(self, ohms):
        if hasattr(self, '_ohms'):
            raise AttributeError('Can\'t set attribute') # 抛出错误，防止父类的属性被修改
        self._ohms = ohms
    



# --------------------TEST CODE------------------------

if __name__ == '__main__':
    r2 = VoltageResistance(1e3)
    print(r2.current)
    r2.voltage = 10
    print(r2.current)

    r3 = BoundedResistance(2)
    print(r3.ohms)

    r4 = FixedResistance(2)
    print(r4.ohms)









    