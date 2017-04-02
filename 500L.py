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
    def isinstance(self,cls):
        return self.cls.issubclass(cls)
    def issubclass(self,cls):
        return cls in self.method_resolution_order()
    def method_resolution_order(self):
        if self.base: return [self] + self.base.method_resolution_order()
        else: return [self]

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

def test_rw_instance_fields():
    ' test object (instance) fields r/w '
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
    ' test class (static) fields r/w'
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

def test_isinstance():
    ' test instance checking /with inheritance/ '
    # python
    class A(object): pass
    class B(A): pass
    b = B()
    assert isinstance(b,B)
    assert isinstance(b,A)
    assert isinstance(b,object)
    assert not isinstance(b,type)
    # object model
    A = Class('A',base=OBJECT,meta=TYPE)
    B = Class('B',base=A,meta=TYPE)
    b = Instance(B)
    assert b.isinstance(B)
    assert b.isinstance(A)
    assert b.isinstance(OBJECT)
    assert not b.isinstance(TYPE)

def test_call_simple():
    ' call in simple single inheritance model '
    # python
    class A(object):
        def f(self): return self.x + 1
    obj = A()
    obj.x = 1
    assert obj.f() == 2
    class B(A): pass
    obj = B()
    obj.x = 1
    assert obj.f() == 2
    # object model
    def f_A(self): return self.Rattr('x') + 1 # dummy function in python
    A = Class('A',base=OBJECT,meta=TYPE,fields={'f':f_A})
    obj = Instance(A)
    obj.Wattr('x',1)
    assert obj.call('f') == 2