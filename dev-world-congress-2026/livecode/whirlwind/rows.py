"""
row polymorphism.

a record type can be open, ending in a row variable that stands for "any
other fields". a function wanting `{ name: Str | r }` accepts any record
that has a Str `name`, whatever else it carries.

real systems such as purescript, elm, ur/web do full row unification, forbid
duplicate labels, and infer the row variable. this toy checks structural
containment against a target record. main insight is that the row variable
absorbs the caller's extra fields.
"""

from dataclasses import dataclass
from typing import Union, Optional


@dataclass(frozen=True)
class Base:
    name: str


@dataclass(frozen=True)
class Record:
    fields: tuple # ((label, Ty), ...)
    rest: Optional[str] = None # row variable name, or None for a closed record


Ty = Union[Base, "Record"]


# main insight: does `have` satisfy `want`?
# `want` may be open, in which case its row variable absorbs have's extras.

def satisfies(have: Record, want: Record) -> bool:
    h = dict(have.fields)
    for label, ty in want.fields:
        if label not in h:
            raise TypeError(f"missing field {label!r}")
        if h[label] != ty:
            raise TypeError(f"field {label!r}: {show(h[label])} != {show(ty)}")
    extra = set(h) - {el for el, _ in want.fields}
    if extra and want.rest is None:
        raise TypeError(f"closed record has no row variable for {extra}")
    return True # want.rest absorbs `extra`


def show(t: Ty) -> str:
    match t:
        case Base(n):
            return n
        case Record(fs, rest):
            inner = ", ".join(f"{el}: {show(ty)}" for el, ty in fs)
            return "{" + inner + (f" | {rest}" if rest else "") + "}"


# demo

if __name__ == "__main__":
    Str = Base("Str")
    Int = Base("Int")

    # greet wants { name: Str | r }
    # which is any record with a Str `name`
    want = Record((("name", Str),), rest="r")

    user = Record((("name", Str), ("age", Int))) # has an extra `age`
    print(f"{show(user)}  satisfies  {show(want)}?", satisfies(user, want))

    anon = Record((("age", Int),)) # no `name`
    try:
        satisfies(anon, want)
    except TypeError as e:
        print("rejected:", e)
