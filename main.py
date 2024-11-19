from typing import Any, Callable


class Base:
    def __init__(self):
        self.events = {}

        for base in reversed(self.__class__.__mro__):
            for elem, value in base.__dict__.items():
                try:
                    getattr(value, "__some_var__")
                except AttributeError:
                    continue
                else:

                    def foo(*args):
                        print(f"{elem=}")
                        print(f"{value=}")
                        print(f"{args=}")
                        print(f"{self.events=}")
                        return value(self, *args)

                    self.events[elem] = foo  # lambda *args: value(self, *args)


def add_event[T: Callable[..., Any]](func: T) -> T:
    setattr(func, "__some_var__", True)
    return func


class Sub(Base):
    @add_event
    def test(self):
        print("hi")


sub = Sub()
for event, func in sub.events.items():
    print(f"Running {event}")
    func()
