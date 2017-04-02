# http://www.aosabook.org/en/500L/a-simple-object-model.html

class Base(object):
    tag = 'Base'
    def __init__(self, name, base=None, meta=None, fields={}):
        self.name = name ; self.base = base ; self.meta = meta
        self.fields = fields
    def __repr__(self):
        return '%s:%s'%(self.tag,self.name)
#         return '[ %s:%s base:%s meta:%s ]' % \
#             (self.tag, self.name, self.base, self.meta)

class Class(Base): tag = 'Class' 

class Instance(Base):
    tag = 'Instance'
#     def __init__(self,base): Base.__init__(self, base.name, base, base.meta)
    
OBJECT = Class('Object')
TYPE = Class('Type')

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
    A = Class(name='A',base=OBJECT,meta=TYPE)
    assert '%s' % A == 'Class:A'
    obj = Instance(A)
    assert '%s' % obj == 'Instance:Class:A'
