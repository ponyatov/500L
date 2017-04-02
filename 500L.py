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
        Base.__init__(self, cls, {})
    def __repr__(self):
        return '%s:%s' % (self.__class__.__name__, self.cls)
    
OBJECT = None#Class('Object')
TYPE = None#Class('Type')

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
    A = Class(name='A', base=OBJECT, meta=TYPE)
    assert '%s' % A == 'Class:A'
    obj = Instance(A)
    assert '%s' % obj == 'Instance:Class:A'
    obj.Wattr('a', 1)
    assert obj.Rattr('a') == 1