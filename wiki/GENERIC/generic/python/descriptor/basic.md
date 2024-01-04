## Description  
### Descriptor HowTo Guide  
[https://docs.python.org/3.12/howto/descriptor.html#descriptor-howto-guide](https://docs.python.org/3.12/howto/descriptor.html#descriptor-howto-guide)  

descriptor - 
[https://docs.python.org/3.12/glossary.html#term-descriptor](https://docs.python.org/3.12/glossary.html#term-descriptor)

```cfgrlanguage
Note:
class dict - stored description as a public attribute;
instance dict - stored actual data as a private attribute.
```

```cfgrlanguage
Note:
descriptor - class
dot operator - lookup atribut in class dict
```

```
class Descriptor:
    
    def__get__(
        self: 'MyClass.atribut = Descriptor()',
        obj: 'my_instance = MyClass()',
        objtype: 'class MyClass'
        ):
        return 'Hello, Word!'

class MyClass:
    atribut = Descriptor()'

my_instance = MyClass()
my_instance.atribut
=> 'Hello, Word!'
```

```cfgrlanguage
Note:

class Descrition:
    def __get__(self, obj, objtype=None):
        value = obj.atribut
        return value
    
    def __set__(self, obj, value):
        obj.atribut = value             # Has't return

class MyClass:
    atribut = Description()
    
class dict - stored description as a public attribute;
instance dict - stored actual data as a private attribute.
```
