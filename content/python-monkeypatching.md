Title: Python monkey patching (for readability)
Date: 2019-02-04 17:09
Category: code
Tags: code, python


When preparing a [Jupyter](https://jupyter.org/) notebook for a workshop on recommendation engines which I’ve presented with a colleague, I was faced with the following problem:

> How to break a large class definition into several cells so it can be presented step-by-step.

Having the ability to declare a rather complex (and large) Python class in separate cells has several advantages, the obvious one being the ability to fully document each method’s functionality with Markdown, rather than comments.

Python does allow for functionality to be added to classes after their declaration via the assignment of methods through attributes. This is commonly known as “monkey patching” and hinges on the concepts of _bound_ and _unbound_ methods. 

I will show a quick and general overview of the methods that Python puts at our disposal for dynamic runtime object manipulation, but for a more in-depth please consult the official [Python documentation](https://docs.python.org/3/).

## Bound and unbound methods

Let’s first look at bound methods. If we assume a class called `Class` and an instance `instance`, with an instance method `bound` and class method `unbound` such that

```python
class Class:
	def bound(self):
		pass
	@staticmethod
	def unbound():
		pass

instance = Class()
```

Then `foo` is a bound method and `bar` is an unbound method.
This definition, in practice, can be exemplified by the standard way of calling `.foo()`, which is

```python
instance.bound()
```

which in turn is equivalent to

```python
Class.bound(instance)
```

The standard way of calling `unbound` is , similarly

```python
instance.unbound()
```

This, however, is equivalent to

```python
Class.unbound()
```

In the unbound case, we can see there’s no need to pass the class instance. `unbound` is _not bound_ to the class instance.

As mentioned before, Python allow us to change the class attributes at runtime. If we consider a method such as

```python
def newBound(self):
	pass
```

we can then add it to the class, even after declaring it. For instance:

```python
Class.newBound = newBound

instance = Class()
instance.newBound() # Class.newBound(instance)
```

It is interesting to note that any type of function definition will work, since functions are first class objects in Python. As such, if the method can be written as a single statement, a `lambda` could also be used, _i.e._

```python
Class.newBound = lambda self: print("I'm a lambda")
```

A limitation of the “monkey patching” method, is that attributes can only be changed at the class definition level.
As an example, although possible, it is not trivial to add the `.newBound()` method to `instance`.
A solution is to either call the descriptor methods (which allow for instance attribute manipulation), or declare the instance attribute as a `MethodType`.
To illustrate this in our case:

```python
import types
instance.newBound = types.MethodType(newBound, instance)

instance.newBound() # Prints "I'm a lambda"
```

This method is precisely, as mentioned, to change attributes for a specific instance, so in this case, if we try to access the bound method from another instance `anotherInstance`, it would fail

```python
anotherInstance = Class()
anotherInstance.newBound() # fails with AttributeError
```

## Abstract classes

Python supports abstract classes, _i.e._ the definition of "blueprint" classes for which we delegate the concrete implementation of abstract methods to subclasses. In Python 3.x this is done via the `@abstractmethod` annotation. If we declare a class such as

```python
from abc import ABC, abstractmethod

class AbstractClass(ABC):
	@abstractmethod
	def abstractMethod(self):
		pass
```

we can then implement `abstractMethod` in all of `AbstractClass`'s subclasses: 

```python
class ConcreteClass(AbstractClass):
    def abstractMethod(self):
        print("Concrete class abstract method")
```

We could, obviously, do this in Python _without_ abstract classes, but this mechanism allows for a greater safety, since implementation of abstract methods is mandatory in this case. With regular classes, not implementing `abstractMethod` would simply assume we were using the parent's definition.

Unfortunately, monkey patching of abstract methods is not supported in Python. We _could_ monkey patch the concrete class:

```python
ConcreteClass.newBound = lambda self: print("New 'child' bound")
c = ConcreteClass()
c.newBound() # prints "New 'child' bound"
```

And we could even add a new bound method to the superclass, which will be available to all subclasses:

```python
AbstractClass.newBound = lambda self: print("New 'parent' bound")
c = ConcreteClass()
c.newBound() # prints "New 'parent' bound"
```

However, we can't add abstract methods with monkey patching. This is [a documented exception](https://docs.python.org/3/library/abc.html#abc.abstractmethod) of this functionality with the specific warning that

> Dynamically adding abstract methods to a class, or attempting to modify the abstraction status of a method or class once it is created, are not supported. The abstractmethod() only affects subclasses derived using regular inheritance; “virtual subclasses” registered with the ABC’s register() method are not affected.

## Private methods

We can dynamically add and replace inner methods, such as:

```python
class Class:
    def _inner(self):
        print("Inner bound")
    def __private(self):
        print("Private bound")
    def callNewPrivate(self):
        self.__newPrivate()
        
Class._newInner = lambda self: print("New inner bound")
c = Class()
c._inner() # prints "Inner bound"
c._newInner() # prints "New inner bound"
```
However, private methods behave differently. Python enforces name mangling for private methods. As specified in the documentation:

> Since there is a valid use-case for class-private members (namely to avoid name clashes of names with names defined by subclasses), there is limited support for such a mechanism, called name mangling. Any identifier of the form `__spam` (at least two leading underscores, at most one trailing underscore) is textually replaced with `_classname__spam`, where classname is the current class name with leading underscore(s) stripped. This mangling is done without regard to the syntactic position of the identifier, as long as it occurs within the definition of a class.

We can then still access the private methods (although we probably shouldn't), but monkey patching won't work as before due to the above.

```python
c._Class__private() # Private bound
Class.__newPrivate = lambda self: print("New private bound")

c = Class()
c._Class__newPrivate() # fails with AttributeError
```

We have defined a new method called `__newPrivate()` but interestingly, this method is _not_ private. We can see this by calling it directly (which is allowed) and by calling the new "private" method from inside the class as `self.__newPrivate()`:

```
c.__newPrivate() # prints "New private bound"
c.callNewPrivate() # fails with AttributeError (can't find _Class_NewPrivate)

```

It is possible to perform some OOP abuse and declare the private method by mangling the name ourselves. In this case we could then do:

```
Class._Class__newPrivate = lambda self: print("New private bound")

c = Class()
c._Class__newPrivate() # prints "New private bound"
c.callNewPrivate() # prints "New private bound"
```

## Conclusion

“Monkey patching” is usually, and rightly so, considered a code smell, due to the increased indirection and potential source of unwanted surprises.
However, having the ability to “monkey patch” classes in Python allows us to write Jupyter notebooks in a more literate, fluid way rather than presenting the user with a “wall of code”.

Thank you for reading. If you have any comments or suggestions please drop me a message on [Mastodon](https://mastodon.technology/@ruivieira).
