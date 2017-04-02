# http://www.aosabook.org/en/500L/a-simple-object-model.html

class Class:
    def __init__(self, name): self.name = name
    def __repr__(self): return '%s:%s' % (self.__class__.__name__, self.name)

def test_rw_field():
    # Python
    class A(object): pass
    obj = A()
    obj.a = 1
    assert obj.a == 1
    obj.b = 5
    assert obj.a == 1
    assert obj.b == 5
    # SOM
    A = Class('A') ; assert '%s' % A == 'Class:Az'
