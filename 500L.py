# http://www.aosabook.org/en/500L/a-simple-object-model.html

class Base(object):
    ' The base class that all of the object model classes inherit from '
    def __init__(self, cls, fields):
        self.cls = cls ; self._fields = fields
    def __repr__(self):
        return '%s:%s' % (self.__class__.__name__, self.name)
    def Wattr(self, fldname, value):
        self.Wdict(fldname, value)
    def Rattr(self, fldname):
        return self.Rdict(fldname)        
    def Wdict(self, fldname, value):
        self._fields[fldname] = value
    MISSING = object()
    def Rdict(self, fldname):
        return self._fields.get(fldname, self.MISSING)

class Class(Base):
    ' A User-defined class '
    def __init__(self, name, base, meta, fields={}):
        Base.__init__(self, meta, fields)
        self.name = name
        self.base = base

class Instance(Base):
    ' Instance of a user-defined class '
    def __init__(self,cls):
        assert isinstance(cls, Class)
        Base.__init__(self, cls, {})
    def __repr__(self):
        return '%s:%s' % (self.__class__.__name__, self.cls)
    
OBJECT = Class('Object', base=None, meta=None)
TYPE = Class('Type', base=OBJECT, meta=None)
# TYPE is an instance of itself
TYPE.cls = TYPE
# OBJECT is an instance of TYPE
OBJECT.cls = TYPE

def test_rw_field():
    # Python
    class A(object): pass
    obj = A()
    obj.a = 1
    assert obj.a == 1
    obj.b = 5
    assert obj.a == 1
    assert obj.b == 5
    obj.a = 2
    assert obj.a == 2
    assert obj.b == 5
    # SOM
    A = Class(name='A', base=OBJECT, meta=TYPE)
    assert '%s' % A == 'Class:A'
    obj = Instance(A)
    assert '%s' % obj == 'Instance:Class:A'
    obj.Wattr('a', 1)
    assert obj.Rattr('a') == 1
    obj.Wattr('b',5)
    assert obj.Rattr('a') == 1
    assert obj.Rattr('b') == 5
    obj.Wattr('a', 2)
    assert obj.Rattr('a') == 2
    assert obj.Rattr('b') == 5
    
def test_rw_class_fields():
    # Python
    class A(object): pass
    A.a = 1
    assert A.a == 1
    A.a = 6
    assert A.a == 6
    # object model
    A = Class('A', base=OBJECT, meta=TYPE, fields={'a':1})
    assert A.Rattr('a') == 1
    A.Wattr('a', 6)
    assert A.Rattr('a') == 6
