"""
gradual typing.

the dynamic type `?` (Dyn) is *consistent* with every type (you might know it as
`Any`). consistency (~) is like equality, except `?` matches anything, and
it is lifted through function types: Fn(a, b) ~ Fn(c, d) iff a ~ c and
b ~ d. consistency is reflexive and symmetric but NOT transitive.

real systems like typescript or typed racket insert runtime
casts where `?` meets a static type, so liars are caught red-handed.
this toy only decides the static consistency relation and inserts no
casts.
"""

from dataclasses import dataclass
from typing import Union

@dataclass(frozen=True)
class Dyn:
    pass # the dynamic type:  ?


@dataclass(frozen=True)
class Base:
    name: str


@dataclass(frozen=True)
class Fn:
    arg: "Ty"
    ret: "Ty"


Ty = Union[Dyn, Base, Fn]


# the consistency relation  ~

def consistent(a: Ty, b: Ty) -> bool:
    match (a, b):
        case (Dyn(), _) | (_, Dyn()):
            return True # ? ~ anything is always consistent
        case (Base(x), Base(y)):
            return x == y
        case (Fn(a1, b1), Fn(a2, b2)):
            return consistent(a1, a2) and consistent(b1, b2)
        case _:
            return False


def show(t: Ty) -> str:
    match t:
        case Dyn():
            return "?"
        case Base(n):
            return n
        case Fn(a, b):
            return f"({show(a)} -> {show(b)})"

# demo

if __name__ == "__main__":
    Int = Base("Int")
    Str = Base("Str")

    def report(a, b):
        print(f"{show(a):16} ~ {show(b):16} : {consistent(a, b)}")

    report(Int, Dyn())                     # True   ? matches anything
    report(Fn(Int, Int), Fn(Dyn(), Dyn())) # True   lifted through ->
    report(Int, Str)                       # False  distinct base types
    report(Int, Fn(Int, Int))              # False  base vs function

    # consistency is not transitive
    # Int ~ ?  and  ? ~ Str,  yet Int !~ Str
    print("not transitive -> Int ~ Str:", consistent(Int, Str))
