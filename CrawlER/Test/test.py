

class A(object):

    name = "杨"


class TestMeta(type):

    def __new__(mcs, name, bases, attrs):

        if name == "A":
            return type.__new__(mcs, name, bases, attrs)

        attrs.update({"age": 12})
        return type.__new__(mcs, name, bases, attrs)


class B(A, metaclass=TestMeta):
    n = 5


b = B()
print(b.name)
print(b.age)